import numpy as np
import torch
from torch.autograd import Variable
import torchvision
from torchvision import transforms

CIFAR_CLASSES = (
    "beaver", "dolphin", "otter", "seal", "whale",
    "aquarium fish", "flatfish", "ray", "shark", "trout",
    "orchids", "poppies", "roses", "sunflowers", "tulips",
    "bottles", "bowls", "cans", "cups", "plates",
    "apples", "mushrooms", "oranges", "pears", "sweet peppers",
    "clock", "computer keyboard", "lamp", "telephone", "television",
    "bed", "chair", "couch", "table", "wardrobe",
    "bee", "beetle", "butterfly", "caterpillar", "cockroach",
    "bear", "leopard", "lion", "tiger", "wolf",
    "bridge", "castle", "house", "road", "skyscraper",
    "cloud", "forest", "mountain", "plain", "sea",
    "camel", "cattle", "chimpanzee", "elephant", "kangaroo",
    "fox", "porcupine", "possum", "raccoon", "skunk",
    "crab", "lobster", "snail", "spider", "worm",
    "baby", "boy", "girl", "man", "woman",
    "crocodile", "dinosaur", "lizard", "snake", "turtle",
    "hamster", "mouse", "rabbit", "shrew", "squirrel",
    "maple", "oak", "palm", "pine", "willow",
    "bicycle", "bus", "motorcycle", "pickup truck", "train",
    "lawn-mower", "rocket", "streetcar", "tank", "tractor"
)

TRN_TRANSFORM = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor()
])
TST_TRANSFORM = transforms.Compose([
    transforms.ToTensor()
])


class LearnedTransform():
    def __init__(self, model):
        self.model = model

    def __call__(self, x):
        x = Variable(x)
        return self.model.transform(x)


def get_cifar_dataset(trn_transform=TRN_TRANSFORM, tst_transform=TST_TRANSFORM):
    # transform code modified from https://github.com/ne7ermore/torch-light/blob/master/DenseNet/train.py
    trans = [transforms.RandomHorizontalFlip(),
             transforms.RandomCrop(32, padding=4),
             transforms.ToTensor()]
    trans = transforms.Compose(trans)
    trainset = torchvision.datasets.CIFAR100(root='data/',
                                             train=True, download=True, transform=trn_transform)

    testset = torchvision.datasets.CIFAR100(root='data/',
                                            train=False, download=True, transform=tst_transform)

    return trainset, testset


def get_cifar_loader(trainset, testset, batch_size=64):
    trainloader = torch.utils.data.DataLoader(
        trainset, batch_size=batch_size, shuffle=True, num_workers=2)

    testloader = torch.utils.data.DataLoader(
        testset, batch_size=batch_size, shuffle=False, num_workers=2)
    return trainloader, testloader


def get_mnist_dataset(trn_size=60000, tst_size=10000):
    MNIST_MEAN = np.array([0.1307, ])
    MNIST_STD = np.array([0.3081, ])
    normTransform = transforms.Normalize(MNIST_MEAN, MNIST_STD)
    trainTransform = transforms.Compose([
        transforms.ToTensor(),
        # normTransform
    ])
    testTransform = transforms.Compose([
        transforms.ToTensor(),
        # normTransform
    ])

    trainset = torchvision.datasets.MNIST(root='../data', train=True,
                                          download=True, transform=trainTransform)
    trainset.train_data = trainset.train_data[:trn_size]
    trainset.train_labels = trainset.train_labels[:trn_size]
    testset = torchvision.datasets.MNIST(root='../data', train=False,
                                         download=True, transform=testTransform)
    testset.test_data = testset.test_data[:tst_size]
    testset.test_labels = testset.test_labels[:tst_size]
    return trainset, testset


def get_mnist_loader(trainset, testset, batch_size=128):
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
                                              shuffle=True, num_workers=2)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
                                             shuffle=False, num_workers=2)

    return trainloader, testloader
