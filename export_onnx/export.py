from ultralytics import YOLO

models=['yolov8n-grass']

types={
    '1':'',
    '2':'torchscript',
    '3':'onnx',
    '4':'openvino',
    '5':'engine',
    '6':'coreml',
}

type_index='3'

for model_name in models:
    model = YOLO(f'../pt/{model_name}.pt')  # load a custom trained model

    # Export the model
    model.export(format=types[f'{type_index}'],batch=32,device='0')