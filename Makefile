.PHONY: start
start: venv
	venv/bin/python -m war_chess_referee

.PHONY: venv
venv:
	mkdir -p models
	curl -sSL https://github.com/ouyanghuiyu/chineseocr_lite/raw/master/models/crnn_lite_lstm_dw_v2.pth > models/crnn_lite_lstm_dw_v2.pth
	virtualenv --python=python3.6 venv
	venv/bin/pip install -r requirements.txt
