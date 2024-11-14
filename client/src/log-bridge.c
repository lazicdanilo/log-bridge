#include "log-bridge.h"
#include <stddef.h>
#include <stdio.h>

static LOG_BRIDGE_PRINT log_bridge_send_fn = NULL;
static struct log_bridge_msg log_bridge_msg = {0};
static volatile uint8_t log_paused = 0;

#if ENABLE_LOG_BRIDGE

/**
  * @brief Initializes the log bridge
  * @param[in] print_fn Function to print the log message
  */
void
log_bridge_init(LOG_BRIDGE_PRINT print_fn) {
    log_bridge_send_fn = print_fn;
}

/**
  * @brief Sends the log message
  * @param[in] log_level Log level
  * @param[in] msg Log message
  */
void
log_bridge_send(log_lvl_t log_level, char* msg, ...) {
    va_list args = {0};

    if (log_paused) {
        return;
    }

    log_bridge_msg.lvl = log_level;

    va_start(args, msg);
    vsnprintf((char*)log_bridge_msg.msg, LOG_BRIDGE_MESSAGE_SIZE, msg, args);
    va_end(args);

    if (log_bridge_send_fn != NULL) {
        log_bridge_send_fn(&log_bridge_msg);
    }
}

/**
  * @brief Pauses the log
  */
void
log_bridge_pause() {
    log_paused = 1;
}

/**
  * @brief Resumes the log
  */
void
log_bridge_resume() {
    log_paused = 0;
}

#endif /* ENABLE_LOG_BRIDGE */
