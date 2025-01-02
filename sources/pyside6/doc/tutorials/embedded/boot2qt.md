(tutorial_boottoqt_raspberrypi)=

# Deploying a PySide6 Application to Boot to Qt on Raspberry Pi

This tutorial provides a step-by-step guide to setting up Boot to Qt on a Raspberry Pi and deploying
a PySide6 application. You will learn how to download and flash the Boot to Qt image, create a
sample PySide6 application, and manually deploy it to the Raspberry Pi. Additionally, the tutorial
covers automating the deployment process with a shell script and offers tips for improving the
manual deployment steps.

> **Note**: This tutorial was tested on Unix hosts. Windows hosts might not work as expected.

> **Note**: Boot to Qt comes with PySide6 pre-installed in its Python environment, so you can start
> developing and deploying PySide6 applications right away without needing to install additional
> packages. Each first minor release of Qt for Device Creation (eg: 6.8.0) does not include PySide6.
> The further sub-releases (eg: 6.8.1, 6.8.2) includes PySide6.

## Prerequisites

- Raspberry Pi 4/5 (aarch64)
- SD card to flash the Boot to Qt image
- `ssh` and `scp` tools available
- Network connectivity between your computer and the Raspberry Pi
- Read the [Boot to Qt Quick Start for Raspberry Pi][boot2qt-quick-start] guide

## Setting Up Boot to Qt on Raspberry Pi

1. **Download Boot to Qt Image**
   - Obtain the Boot to Qt image for Raspberry Pi as mentioned using the Qt maintenance tool in
     [Installing Boot to Qt Software Stack][installing-boot2qt]
   - Ensure the image you downloaded has PySide6 pre-installed in the Python environment.

2. **Flash the Image to an SD Card**
   - Use Qt Creator to flash the Boot to Qt image to an SD card by following the instructions in
     [Flashing the Image to an SD Card][flashing-image]
   - Alternatively, use a tool like `balenaEtcher` or `dd` to write the image download in step 1 to
     the SD card.
   - **Using balenaEtcher:**
     1. Download and install balenaEtcher from [balena.io][balenaetcher].
     2. Open balenaEtcher.
     3. Select the Boot to Qt image file.
     4. Select the target SD card.
     5. Click "Flash!" to start the process.
   - **Using `dd`:**
     1. Identify the SD card device name using `lsblk` or `fdisk -l`.
     2. Unmount the SD card partitions.
     3. Write the image to the SD card using `dd`:

        ```sh
        sudo dd if=<path-to-image-file> of=/dev/sdX bs=4M status=progress
        ```
     > **Warning:** Ensure you replace `/dev/sdX` with the correct device name of the SD card.

3. **Boot the Raspberry Pi**
   - Insert the newly flashed SD card into the Raspberry Pi.
   - Power on your device (make sure you are connected to the network)

4. **Verify Boot to Qt is Running**
   - Ensure the Raspberry Pi boots into Boot to Qt. The device starts with Boot to Qt Demo Launcher
     application by default. The IP address is shown if the device is connected to an Ethernet or
     Wi-Fi network, or to the host computer via USB OTG.
   - You can check network connectivity by pinging the device.

## Preparing the PySide6 Application

1. **Create a Sample PySide6 Application**
   - Write a simple PySide6 application:

     ```python
     # sample_app.py
     import sys
     from PySide6.QtWidgets import QApplication, QLabel

     app = QApplication(sys.argv)
     label = QLabel("Hello from PySide6 on Boot to Qt!")
     label.show()
     sys.exit(app.exec())
     ```

2. **Test Locally**
   - Run the application on your development machine to ensure it works.

     ```sh
     python sample_app.py
     ```
    > **Note:** Make sure you have PySide6 installed on your local environment. If not, you can install
    > it using `pip`: `pip install PySide6`.


## Deploying the Application to Boot to Qt

1. **Find the Raspberry Pi's IP Address**
   - For finding the IP Address of the device, refer to the section `Verify Boot to Qt is Running`.

2. **Transfer the Application Using `scp`**
   - Copy the application to the Raspberry Pi:

     ```sh
     scp sample_app.py username@<RASPBERRY_PI_IP>:
     ```
    > **Note:** This command copies the file to the home directory of the user `username`. You can
    > specify a different directory if needed.

3. **SSH into the Raspberry Pi**
   - Connect to the Raspberry Pi via SSH:

     ```sh
     ssh username@<RASPBERRY_PI_IP>
     ```

4. **Run the Application on the Raspberry Pi**
   - Execute the application:

     ```sh
     python3 /home/username/sample_app.py
     ```

## Automating Deployment with a Shell Script

You can streamline the deployment process with a shell script.

```sh
#!/bin/bash

# Variables
APP_NAME="sample_app.py"
PI_USER="username"
PI_IP="<RASPBERRY_PI_IP>"
REMOTE_PATH="/home/username/"

# Copy the application to the Raspberry Pi
scp $APP_NAME $PI_USER@$PI_IP:$REMOTE_PATH

# Run the application on the Raspberry Pi
ssh $PI_USER@$PI_IP "python3 $REMOTE_PATH$APP_NAME"
```

- **Make the Script Executable**

  ```sh
  chmod +x deploy.sh
  ```

- **Run the Script**

  ```sh
  ./deploy.sh
  ```

## Improving the Manual Deployment Steps

Although SSH and SCP are effective, you can enhance the deployment process:

- **Use SSH Key Authentication**
  - Set up SSH keys to avoid entering passwords each time and use `ssh-copy-id` tool to copy the
    public key to the Raspberry Pi.

- **Use `rsync` for Efficient File Transfer**
  - Alternative to `scp` for transferring files.
  - `rsync` only transfers changed files.

    ```sh
    rsync -avz sample_app.py username@<RASPBERRY_PI_IP>:
    ```
    > **Note:** This command copies the file to the home directory of the user `username`.

## Conclusion

In this tutorial, we have provided a comprehensive guide to setting up Boot2Qt on a Raspberry Pi and
deploying a PySide6 application.

[boot2qt-quick-start]: https://doc.qt.io/Boot2Qt/b2qt-qsg-raspberry.html
[installing-boot2qt]: https://doc.qt.io/Boot2Qt/b2qt-qsg-raspberry.html#installing-boot-to-qt-software-stack-using-qt-maintenance-tool
[flashing-image]: https://doc.qt.io/Boot2Qt/b2qt-qsg-raspberry.html#installing-boot-to-qt-on-the-target-device
[qt-creator]: https://doc.qt.io/qtcreator
[balenaetcher]: https://etcher.balena.io/
