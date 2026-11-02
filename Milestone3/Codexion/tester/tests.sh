#!/bin/bash

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

EXEC="./codexion"

TESTS_RUN=0
TESTS_PASSED=0

print_header() {
    echo -e "\n${CYAN}================================================================${NC}"
    echo -e "${MAGENTA}  $1${NC}"
    echo -e "${CYAN}================================================================${NC}"
}

test_invalid_args() {
    ((TESTS_RUN++))
    echo -en "${YELLOW}Test ${TESTS_RUN}:${NC} $EXEC $* "

    timeout 15 "$EXEC" "$@" > tmp.log 2>&1
    local exit_code=$?

    if [ $exit_code -eq 124 ]; then
        echo -e "\n   ${RED}[KO] (Timeout - program hangs instead of returning an error!)${NC}"
    elif [ $exit_code -ne 0 ]; then
        echo -e "\n   ${GREEN}[OK] (Correctly rejected)${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "\n   ${RED}[KO] (Program ACCEPTED invalid arguments and returned code 0!)${NC}"
    fi
}

test_valid_args() {
    ((TESTS_RUN++))
    echo -en "${YELLOW}Test ${TESTS_RUN}:${NC} $EXEC $* "

    timeout 5 "$EXEC" "$@" > tmp.log 2>&1
    local exit_code=$?

    if [ $exit_code -eq 124 ]; then
        echo -e "\n   ${RED}[KO] (Timeout - DEADLOCK or hangs!)${NC}"
    elif [ $exit_code -eq 0 ]; then
        echo -e "\n   ${GREEN}[OK] (Correctly accepted valid arguments)${NC}"
        ((TESTS_PASSED++))
    else
        echo -e "\n   ${RED}[KO] (Program REJECTED valid arguments!)${NC}"
    fi
}

test_sim() {
    ((TESTS_RUN++))
    local expected="$1"
    shift

    local num_coders="$1"
    local num_compiles="$6"

    echo -e "${YELLOW}Test ${TESTS_RUN}:${NC} $EXEC $*"
    echo -en "   Expected: ${expected}..."

    timeout 30 "$EXEC" "$@" > tmp.log 2>&1
    local exit_code=$?

    local died=$(grep -c "burned out" tmp.log)
    local got_dongles=$(grep -c "has taken a dongle" tmp.log)
    local got_compiles=$(grep -c "is compiling" tmp.log)
    local got_debugs=$(grep -c "is debugging" tmp.log)
    local got_refactors=$(grep -c "is refactoring" tmp.log)

    local exp_compiles=0
    local exp_dongles=0
    if [[ "$num_compiles" =~ ^-?[0-9]+$ ]]; then
        exp_compiles=$((num_coders * num_compiles))
        exp_dongles=$((exp_compiles * 2))
    fi

    local stats_msg="\n   ${CYAN}(Dongles: ${got_dongles}/${exp_dongles}, Compiles: ${got_compiles}/${exp_compiles}, Debugs: ${got_debugs}/${exp_compiles}, Refactors: ${got_refactors}/${exp_compiles})${NC}"

    if [ $exit_code -eq 124 ]; then
        echo -e "\n   ${RED}[KO] (Timeout - DEADLOCK! Simulation hangs forever!)${NC}"
        return
    fi

    if [ "$expected" == "DEATH" ]; then
        local last_line=$(awk '/[^[:space:]]/{last=$0} END{print last}' tmp.log)
        local is_last=0
        if [[ "$last_line" == *"burned out"* ]]; then
            is_last=1
        fi

        if [ $died -eq 1 ] && [ $is_last -eq 1 ]; then
            echo -e "\n   ${GREEN}[OK] (Exactly 1 burnout, and it is the last line!)${NC} $stats_msg"
            ((TESTS_PASSED++))
        elif [ $died -ne 1 ]; then
            echo -e "\n   ${RED}[KO] (Expected EXACTLY 1 death, but got $died! Exit: $exit_code)${NC} $stats_msg"
        else
            echo -e "\n   ${RED}[KO] (Burnout occurred, but it was NOT the last line! Exit: $exit_code)${NC} $stats_msg"
            echo -e "   ${RED}Last line was: \"$last_line\"${NC}"
        fi

    elif [ "$expected" == "SURVIVE" ]; then
        local stats_match=0
        if [ $got_dongles -eq $exp_dongles ] && [ $got_compiles -eq $exp_compiles ] && [ $got_debugs -eq $exp_compiles ] && [ $got_refactors -eq $exp_compiles ]; then
            stats_match=1
        fi

        if [ $died -eq 0 ] && [ $exit_code -eq 0 ] && [ $stats_match -eq 1 ]; then
            echo -e "\n   ${GREEN}[OK] (Everyone survived, and all action counts match perfectly)${NC} $stats_msg"
            ((TESTS_PASSED++))
        elif [ $died -ne 0 ]; then
            echo -e "\n   ${RED}[KO] (Someone died! Died: $died, Exit: $exit_code)${NC} $stats_msg"
        elif [ $exit_code -ne 0 ]; then
            echo -e "\n   ${RED}[KO] (Program crashed! Exit: $exit_code)${NC} $stats_msg"
        else
            echo -e "\n   ${RED}[KO] (Stats mismatch! Not all actions were completed)${NC} $stats_msg"
        fi

    elif [ "$expected" == "SILENT" ]; then
        if [ $exit_code -eq 0 ]; then
            if [ $got_dongles -eq 0 ] && [ $got_compiles -eq 0 ] && [ $got_debugs -eq 0 ] && [ $got_refactors -eq 0 ] && [ $died -eq 0 ]; then
                echo -e "\n   ${GREEN}[OK] (Perfect silent quit with code 0 and 0 actions executed)${NC} $stats_msg"
                ((TESTS_PASSED++))
            else
                echo -e "\n   ${RED}[KO] (Clean exit, but unexpected actions were logged!)${NC} $stats_msg"
            fi
        else
            echo -e "\n   ${RED}[KO] (Expected silent quit with code 0, but got exit code: $exit_code)${NC} $stats_msg"
        fi
    fi
}

if [ ! -f "$EXEC" ]; then
    echo -e "${RED}Error: $EXEC not found! Run make first.${NC}"
    exit 1
fi

print_header "1. INVALID ARGS TESTS (Should return error)"
test_invalid_args
test_invalid_args 5 800 200 200 70 3 10 fifo 20
test_invalid_args 5 800 200 200 70 3
test_invalid_args 5 800 200 -200 70 3 10 fifo
test_invalid_args 5 800 200 200 70 3 10 wrong_sch
test_invalid_args 5 800 200 2147483649 70 3 10 edf
test_invalid_args -2147483648 20 200 200 70 3 10 fifo
test_invalid_args 5 b a 200 70 3 10 fif
test_invalid_args 5 300 "   " 200 70 3 10 fifo
test_invalid_args 0 300 50 200 70 3 10 fifo
test_invalid_args "" 800 200 200 70 3 10 fifo
test_invalid_args 5 " +0003		7" 200 200 70 3 10 fifo
test_invalid_args + 800 200 200 70 3 10 fifo
test_invalid_args "    +    " 800 200 200 70 3 10 edf
test_invalid_args 5 800 200 200 70 3 10 ""
test_invalid_args 5 800 200 200 70 3 10 FIFO
test_invalid_args 5 800 200 200 70 3 10 EdF
test_invalid_args 2147483648 800 200 200 70 3 10 edf
test_invalid_args 5 800 2147483648 200 70 3 10 fifo
test_invalid_args 300 800 "   + 200 " 200 70 3 10 edf
test_invalid_args 5 800 "   +000" 200 70 -1 10 edf

print_header "2. VALID ARGS TESTS (Should be accepted)"
test_valid_args 5 30 " +777  " 200 70 3 10 fifo
test_valid_args 5 "  +00 	" " 777" "  077" 0 3 0 edf
test_valid_args 5 "  +030" "  	+777	" "  077" 0 3 0 fifo
test_valid_args 00000000005 800 200 200 70 0 10 fifo
test_valid_args 5 "00000800		" 200 200 70 0 10 edf
test_valid_args "	5" " 800" "		200" 200 70 0 10 edf
test_valid_args 1 1 0 0 0 0 0 fifo
test_valid_args 1 0 0 0 0 0 0 fifo

print_header "3. BASIC TESTS"
test_sim "DEATH" 1 800 200 200 200 10 0 fifo
test_sim "DEATH" 21 800 300 300 200 10 20 fifo
test_sim "SURVIVE" 30 350 30 20 10 5 50 edf
test_sim "DEATH" 30 300 30 20 10 5 100 edf
test_sim "SURVIVE" 29 300 30 20 10 5 30 edf
test_sim "SURVIVE" 99 400 70 42 66 10 9 fifo
test_sim "SURVIVE" 200 700 90 65 30 10 20 edf
test_sim "SURVIVE" 399 700 90 65 30 10 20 fifo

print_header "4. COMPLEX TESTS AND EDGE CASES"
test_sim "SILENT" 1 0 0 0 0 0 0 edf
test_sim "SILENT" 200 50 70 80 59 0 30 edf
test_sim "DEATH" 3 40 50 0 0 2 0 fifo
test_sim "DEATH" 3 60 50 0 0 2 0 fifo
test_sim "SURVIVE" 3 160 50 0 0 2 0 edf
test_sim "SURVIVE" 199 600 5 5 5 10 0 edf
test_sim "DEATH" 199 4 5 5 5 10 0 fifo
test_sim "DEATH" 50 0 10 0 0 1 0 fifo
test_sim "DEATH" 4 200 205 0 0 1 0 edf
test_sim "DEATH" 4 390 200 100 100 2 0 fifo
test_sim "SURVIVE" 4 405 200 100 100 2 0 edf
test_sim "SURVIVE" 200 10000 0 0 0 1000 0 edf
test_sim "SURVIVE" 200 1000 1 0 0 100 0 fifo
test_sim "DEATH" 50 500 10 10 0 10 800000 fifo
test_sim "DEATH" 187 300 10000000 0 0 10 0 edf
test_sim "SURVIVE" 123 3000000 00 0 0 10 0 fifo
test_sim "DEATH" 77 300 10 28456100 0 10 100 fifo
test_sim "DEATH" 189 300 7 5 2 33333 3 fifo
test_sim "DEATH" 5 500 200 200 200 10 0 fifo

print_header "RESULTS"
if [ $TESTS_PASSED -eq $TESTS_RUN ]; then
    echo -e "${GREEN}Success! Passed $TESTS_PASSED / $TESTS_RUN tests! ${NC}\n"
else
    echo -e "${RED}Warning! Passed $TESTS_PASSED / $TESTS_RUN tests. Needs work. ${NC}\n"
fi

rm -f tmp.log