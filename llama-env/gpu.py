import torch
print("CUDA disponible:", torch.cuda.is_available())
print("Dispositivo actual:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "Ninguno")
