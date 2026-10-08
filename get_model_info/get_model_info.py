from ultralytics import YOLO
import os

if __name__ == '__main__':

    file_path=fr"F:\文档\论文\小论文\SW-SegYOLO\实验"

    models_name = os.listdir(file_path)

    for model_name in models_name:
        model_path = os.path.join(file_path, model_name,'weights','best.pt')
        try:
            model = YOLO(model_path)
            model.info(detailed=False)
        except Exception as e:
            print(f"错误：{str(e)}")
