*** Settings ***
Library     ${LIBRARY}.py


*** Variables ***
${LIBRARY}      DynamicLibrary


*** Test Cases ***
Keyword Names
    Keyword In Main
    Function
    FUNCTION
    Method
    Custom Name
    Cust Omna Me
    IF    "$LIBRARY" == "ExtendExistingLibrary"    Keyword In Extending Library

Method Without @keyword Are Not Keyowrds
    [Documentation]    FAIL GLOB:    No keyword with name 'Not Keyword' found.*
    Not Keyword

Arguments
    [Template]    Return value should be
    'foo', 'bar'    Mandatory    foo    bar
    'foo', 'default', 3    Defaults    foo
    'foo', 2, 3    Defaults    foo    ${2}
    'a', 'b', 'c'    Defaults    a    b    c

Named Arguments
    [Template]    Return value should be
    'foo', 'bar'    Mandatory    foo    arg2=bar
    '1', 2    Mandatory    arg2=${2}    arg1=1
    'x', 'default', 'y'    Defaults    x    arg3=y

Varargs And Kwargs
    [Template]    Return value should be
    ${EMPTY}    Varargs and kwargs
    'a', 'b', 'c'    Varargs and kwargs    a    b    c
    a\='1', b\=2    Varargs and kwargs    a=1    b=${2}
    'a', 'b\=b', c\='c'    Varargs and kwargs    a    b\=b    c=c

Embedded Arguments
    [Documentation]    FAIL    Work But This Fails
    Embedded Arguments "work"
    EmbeDded ArgumeNtS "Work But This Fails"


*** Keywords ***
Return Value Should Be
    [Arguments]    ${expected}    ${keyword}    @{args}    &{kwargs}
    ${result}    Run Keyword    ${keyword}    @{args}    &{kwargs}
    Should Be Equal    ${result}    ${expected}
