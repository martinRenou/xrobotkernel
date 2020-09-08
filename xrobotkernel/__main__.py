from ipykernel.kernelapp import IPKernelApp
from . import XRobotKernel

IPKernelApp.launch_instance(kernel_class=XRobotKernel)
