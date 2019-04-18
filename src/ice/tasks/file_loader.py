from luigi import LocalTarget, Task, ExternalTask, Parameter, build
from luigi.contrib.s3 import S3Target


class ContentImage(ExternalTask):
    IMAGE_ROOT = 's3://cscie29-data/pset4/data/'

    image = Parameter()

    def output(self):
        return S3Target(self.IMAGE_ROOT + self.image, format=luigi.format.Nop)

class LocalTargetOutput():
    def __init__(self,filepattern='{task}.txt'):
        self.filename = filepattern.format(task=self.__class__.__name__)
        print(self.filename)

    def __get__(self, instance, owner):
        return lambda : LocalTarget(self.filename)

class Requirement:
    def __init__(self,task_class, **params):
        self.task_class = task_class
        self.params = params

    def __get__(self,task,cls):
        return task.clone(self,self.task_class, **self.params)

class Requires:
    def __get__(self, instance, owner):
        return lambda : self.instance

    def __call__(self,task):
        pass


class MyTask(Task):
    requires = Requires()
    other = Requirement(ContentImage)
    output = LocalTargetOutput()

    def run(self):
        with self.other.output().open(mode='r') as f:
            print(f.read())

build([MyTask(
            model ='rain_princess.pth',
            image = 'luigi.jpg'
        )], local_scheduler=True)
