<div align="center">

# Muhammet Yusuf Özkan

**Embedded Systems · Robotics · Electronics**

Electrical and Electronics Engineering student at Konya Technical University, graduating in 2027.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-yusufozkan1-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/yusufozkan1)
![Location](https://img.shields.io/badge/Location-Konya%2C%20Türkiye-2F855A?style=flat-square)
![Open to Work](https://img.shields.io/badge/Open%20to-Embedded%20%26%20Robotics%20Roles-2F855A?style=flat-square)

</div>

## About

I build embedded and robotic systems close to the hardware: STM32 firmware, real-time control, sensor interfaces, ROS 2 integration, and PCB design.

My recent work includes FreeRTOS-based motor and IMU tasks, micro-ROS communication, differential-drive control, BNO085 integration over SPI, I²C and UART-RVC, and autonomous-navigation systems using ROS 2 Nav2. I also design mixed-signal and power-electronics PCBs in KiCad.

I am currently interested in embedded firmware, electronics design, robotics, autonomous systems, and junior engineering opportunities in Türkiye or abroad.

## Core Technologies

- **Embedded:** C, C++, STM32, STM32 HAL, FreeRTOS, interrupts, PWM, encoders and PID control
- **Interfaces:** UART, SPI, I²C, USB CDC and SWD
- **Robotics:** ROS 2 Humble, micro-ROS, Nav2, sensor integration and differential drive
- **Hardware:** KiCad, schematic capture, two-layer PCB layout, power electronics and hardware bring-up
- **Vision:** Python, OpenCV, YOLOv8 and NVIDIA Jetson

## Selected Projects

### [Dual BNO085 IMUs on a Shared SPI Bus](https://github.com/alcad1us/stm32-dual-bno085-shared-spi)

STM32F407 driver for two BNO085 IMUs sharing one SPI bus. Implements sequential boot, explicit chip selection, defensive transaction handling, SHTP parsing, quaternion-to-Euler conversion, automatic yaw tare and serial health monitoring.

STM32F407 · Embedded C · SPI · BNO085 · SHTP

### [STM32F407 + micro-ROS over USB CDC](https://github.com/alcad1us/stm32f407-microros-usb)

A practical STM32-to-ROS 2 communication baseline using micro-ROS and native USB CDC transport, validated with ROS 2 Humble on Ubuntu.

STM32F407 · micro-ROS · ROS 2 · USB CDC

### [Dual BNO085 UART-RVC Driver](https://github.com/alcad1us/stm32-dual-bno085-uart-rvc)

Interrupt-driven dual-channel UART-RVC driver for two BNO085 sensors on STM32F407. Uses independent UART peripherals and a reusable packet-parsing state machine.

STM32F407 · Embedded C · UART · Interrupts

### [STM32F4 Development Board](https://github.com/alcad1us/stm32f4-dev-board)

A custom STM32F4 development board designed in KiCad, covering power regulation, clocking, decoupling, USB, SWD, schematic capture and two-layer PCB layout.

KiCad · STM32F4 · PCB Design · USB · SWD

### [Underwater YOLO Target Detection](https://github.com/alcad1us/freshman-yolo-shape-detection)

YOLOv8-based target-detection and centering pipeline developed for the TEKNOFEST Unmanned Underwater Vehicle Competition under Jetson Nano compute constraints.

Python · OpenCV · YOLOv8 · Jetson Nano

## Experience

### Embedded Systems Engineer · RACLAB ROVER
**January 2026 – Present**

- Develop STM32-based vehicle-control firmware for an autonomous ground vehicle.
- Work on micro-ROS communication with ROS 2, differential-drive control and FreeRTOS-based motor and IMU tasks.

### Embedded Systems Engineer · RACLAB FAAL
**January 2026 – Present**

- Develop embedded control software for an autonomous load-carrying robot.
- Implemented encoder-feedback PID motor control for differential drive.

### Embedded Systems R&D Intern · Elfatek Teknoloji A.Ş. / AKİBA
**July 2026 – August 2026**

- Worked on embedded hardware projects for autonomous mobile robots.
- Designed a BQ24610-based 4S Li-Po charging board while preserving the existing BMS architecture.
- Completed schematic design, two-layer PCB layout and technical documentation in KiCad.

### Undergraduate Researcher · TÜBİTAK 2209-A
**October 2025 – Present**

Contribute to an AI-assisted autonomous load-carrying robot combining YOLO-based perception, encoder/IMU/LiDAR sensor fusion and ROS 2 Nav2.

## Achievements

- **TEKNOFEST 2026 Unmanned Ground Vehicle Competition — Finalist**, Kapsül RACLAB ROVER
- **TEKNOFEST 2024 Unmanned Underwater Vehicle Competition — Advanced Category Finalist**, YAZGİT BARBAROV
- **TÜBİTAK 2209-A** research project contributor

## Current Focus

- Robust STM32 firmware and real-time embedded systems
- ROS 2 and micro-ROS integration
- Sensor interfaces and autonomous-robot control
- Power electronics and production-oriented PCB design

## Contact

The best way to reach me is through [LinkedIn](https://www.linkedin.com/in/yusufozkan1).

---

*Building reliable systems where firmware, electronics and robotics meet.*
