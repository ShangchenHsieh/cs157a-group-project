import kagglehub

# Download latest version
path = kagglehub.dataset_download("lako65/ssh-brute-force-ipuserpassword")

print("Path to dataset files:", path)
