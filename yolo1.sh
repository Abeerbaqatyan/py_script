yolo1


sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y
python3 -m venv yolov8_env
source yolov8_env/bin/activate
pip install --upgrade pip  
pip install ultralytics  
pip install torch torchvision torchaudio
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
python3 -c "import torch; print(torch._version_)"




ls /dev/video*
ffplay /dev/video
sudo apt install ffmpeg
yolo task=detect mode=predict model=yolov8n.pt source=0 show=True