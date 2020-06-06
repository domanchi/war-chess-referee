from functools import lru_cache

import torch
from PIL import Image
from torchvision import transforms

from .alphabet import alphabetChinese
from .crnn import CRnn
from ..util import get_path_to


class CRNNPredictor:
    def __init__(self):
        # TODO: enable GPU.
        self.device = torch.device('cpu')
        self.net = get_crnn_net().to(self.device)
        self.net.load_state_dict({
            key.replace('module.', ''): value
            for key, value in torch.load(
                get_path_to('models/crnn_lite_lstm_dw_v2.pth'),
                map_location=self.device,
            ).items()
        })
        self.net.eval()
    
    def predict(self, image: Image):
        # Convert to grayscale
        image = image.convert('L')

        # Then, normalize it to a height of 32.
        scale = image.size[1] * 1.0 / 32
        scaled_width = int(image.size[0] / scale)
        image = image.resize((scaled_width, 32,), Image.BILINEAR)

        # Transform it to Tensor, to be used in tensorflow.
        image = transforms.ToTensor()(image).sub(0.5).div(0.5).to(self.device)

        # Finally, run the data through the model.
        predictions = self.net(image.view(1, *image.size()))
        _, indexes = predictions.max(2)

        # We need to lower the dimension, since we increased the dimension before putting
        # it through the neural net.
        indexes = indexes.view(-1)

        output = []
        for i, index in enumerate(indexes):
            if (
                # If it found something
                index > 0 and

                # ...and it isn't the same thing as the previous character
                not (
                    i > 0
                    and indexes[i - 1] == indexes[i]
                )
            ):
                output.append(alphabetChinese[index - 1])

        return ''.join(output)


@lru_cache(maxsize=1)
def get_crnn_net():
    # I honestly don't know what any of these values mean: it's just obtained
    # from https://github.com/ouyanghuiyu/chineseocr_lite/blob/c304cd1/model.py#L22
    return CRnn(
        32,
        1,
        len(alphabetChinese) + 1,
        256,
        n_rnn=2,
        leakyRelu=False,
        lstmFlag=True,
    )