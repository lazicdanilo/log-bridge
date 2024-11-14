# Log Bridge - client

This is a C code that usually runs on MCU. It will communicate with the server (Raspberry Pi, user PC, etc...) via USART. It's up to the user to implement the communication protocol and pass the LOG_BRIDGE_PRINT function callback to the library.

Example of the LOG_BRIDGE_PRINT function callback in STM32CubeIDE:

```c
#include "FreeRTOS.h"
#include "task.h"

void prv_log_bridge_init(struct log_bridge_msg* log_bridge_msg) {
    const char* task_name = NULL;
  
    task_name = pcTaskGetName(xTaskGetCurrentTaskHandle());
    snprintf((char*)log_bridge_msg->thread_name, LOG_BRIDGE_THREAD_NAME_SIZE, "%s", task_name);

    log_bridge_msg->timestamp_ms = xTaskGetTickCount();

    HAL_UART_Transmit_DMA(&huart3, (uint8_t*)log_bridge_msg, sizeof(struct log_bridge_msg));
}
```
