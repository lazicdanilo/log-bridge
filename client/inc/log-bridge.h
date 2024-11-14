#ifndef LOG_BRIDGE_H
#define LOG_BRIDGE_H

#include <stdarg.h> /* Needed for va_start and va_end */
#include <stdint.h>

#define ENABLE_LOG_BRIDGE 1

#define LOG_BRIDGE_MESSAGE_SIZE     128
#define LOG_BRIDGE_THREAD_NAME_SIZE 32

#define LOG_BRIDGE_COMMAND_MSG_SIZE 32

typedef enum {
    LOG_BRIDGE_LVL_NONE = 0,
    LOG_BRIDGE_LVL_DEBUG,
    LOG_BRIDGE_LVL_INFO,
    LOG_BRIDGE_LVL_WARN,
    LOG_BRIDGE_LVL_ERROR,
    LOG_BRIDGE_LVL_FATAL,

    LOG_MSG_LVL_MAX_VAL = 0xFF /* Make sure the enum is 8 bytes */
} log_lvl_t;

#if ENABLE_LOG_BRIDGE
#define LOG_BRIDGE_DEBUG(...) log_bridge_send(LOG_BRIDGE_LVL_DEBUG, __VA_ARGS__);
#define LOG_BRIDGE_INFO(...)  log_bridge_send(LOG_BRIDGE_LVL_INFO, __VA_ARGS__);
#define LOG_BRIDGE_WARN(...)  log_bridge_send(LOG_BRIDGE_LVL_WARN, __VA_ARGS__);
#define LOG_BRIDGE_ERROR(...) log_bridge_send(LOG_BRIDGE_LVL_ERROR, __VA_ARGS__);
#define LOG_BRIDGE_FATAL(...) log_bridge_send(LOG_BRIDGE_LVL_FATAL, __VA_ARGS__);
#define LOG_BRIDGE_PAUSE()    log_bridge_pause();
#define LOG_BRIDGE_RESUME()   log_bridge_resume();
#else /* ENABLE_LOG_BRIDGE */
#define LOG_BRIDGE_INFO(...)
#define LOG_BRIDGE_WARN(...)
#define LOG_BRIDGE_ERROR(...)
#define LOG_BRIDGE_FATAL(...)
#define LOG_BRIDGE_PAUSE(...)
#define LOG_BRIDGE_RESUME(...)
#endif /* ENABLE_LOG_BRIDGE */

/* Log message is generate on client (MCU) and sent to host (PC) */
struct log_bridge_msg {
    log_lvl_t lvl;
    uint32_t timestamp_ms;
    uint8_t thread_name[LOG_BRIDGE_THREAD_NAME_SIZE];
    uint8_t msg[LOG_BRIDGE_MESSAGE_SIZE];
} __attribute__((packed));

/* Command message is generated on host (PC) and sent to client (MCU) */
struct command_msg {
    uint8_t msg[LOG_BRIDGE_COMMAND_MSG_SIZE];
} __attribute__((packed));

typedef void (*LOG_BRIDGE_PRINT)(struct log_bridge_msg* log_bridge_msg);

void log_bridge_init(LOG_BRIDGE_PRINT print_fn);
void log_bridge_send(log_lvl_t log_level, char* msg, ...);
void log_bridge_pause();
void log_bridge_resume();

#endif /* LOG_BRIDGE_H */