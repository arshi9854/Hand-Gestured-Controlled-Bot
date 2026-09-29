#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p build
"${CXX:-c++}" -std=c++11 -Wall -Wextra -Werror -I libraries/GestureControl/src tests/control_test.cpp -o build/control_test
./build/control_test
