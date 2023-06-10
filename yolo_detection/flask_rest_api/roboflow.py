from roboflow import Roboflow
rf = Roboflow(api_key="fJNx9oJEEE4o6DYMMfYC")
project = rf.workspace("project-c6c5q").project("baseballplayer-eni5v")
dataset = project.version(1).download("yolov5")