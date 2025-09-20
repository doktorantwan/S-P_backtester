cmake_minimum_required(VERSION 3.22)

project(quant_min
  VERSION 0.1.0
  LANGUAGES CXX
)

# ---- C++ standard ----
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ---- Default build type (for single-config generators like Ninja/Make) ----
if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose Debug or Release" FORCE)
endif()

# ---- Options you can toggle from the command line ----
option(ENABLE_WARNINGS      "Turn on extra compiler warnings" ON)
option(WARNINGS_AS_ERRORS   "Treat warnings as errors"        OFF)
option(ENABLE_SANITIZERS    "Enable Address/UB sanitizers"    OFF)

# ---- Where to put the built binaries ----
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# ---- Your executable target ----
add_executable(backtest
  src/main.cpp
)

# If you later add headers in include/, expose them like this:
# target_include_directories(backtest PRIVATE ${CMAKE_SOURCE_DIR}/include)

# ---- Warnings configuration (cross-platform) ----
if(ENABLE_WARNINGS)
  if(MSVC)
    target_compile_options(backtest PRIVATE /W4)
    if(WARNINGS_AS_ERRORS)
      target_compile_options(backtest PRIVATE /WX)
    endif()
  else()
    target_compile_options(backtest PRIVATE
      -Wall -Wextra -Wpedantic
      -Wconversion -Wshadow -Wdouble-promotion
    )
    if(WARNINGS_AS_ERRORS)
      target_compile_options(backtest PRIVATE -Werror)
    endif()
  endif()
endif()

# ---- Optional sanitizers for debugging (non-MSVC) ----
if(ENABLE_SANITIZERS AND NOT MSVC)
  target_compile_options(backtest PRIVATE -fsanitize=address,undefined -fno-omit-frame-pointer)
  target_link_options(backtest    PRIVATE -fsanitize=address,undefined)
endif()

# ---- Helpful status message at configure time ----
message(STATUS "Config: ${CMAKE_BUILD_TYPE},
        C++${CMAKE_CXX_STANDARD}, warnings=${ENABLE_WARNINGS},
        werror=${WARNINGS_AS_ERRORS}, sanitizers=${ENABLE_SANITIZERS}")