*** Settings ***
Library        ${LIBRARY}.py

*** Variables ***
${LIBRARY}    DynamicLibrary

*** Test Cases ***
Keyword names
    Keyword in main
    Function
    FUNCTION
    Method
    Custom name
    Cust omna me
    Run Keyword If    $LIBRARY == "ExtendExistingLibrary"
    ...    Keyword in extending library

Method without @keyword are not keyowrds
    [Documentation]    FAIL    No keyword with name 'Not keyword' found.
    Not keyword

Arguments
    [Template]    Return value should be
    'foo', 'bar'           Mandatory    foo    bar
    'foo', 'default', 3    Defaults     foo
    'foo', 2, 3            Defaults     foo    ${2}
    'a', 'b', 3            Defaults     a    b    3

Named arguments
    [Template]    Return value should be
    'foo', 'bar'           Mandatory    foo    arg2=bar
    '1', 2                 Mandatory    arg2=${2}    arg1=1
    'x', 'default', 4      Defaults     x    arg3=4

Varargs and kwargs
    [Template]    Return value should be
    ${EMPTY}               Varargs and kwargs
    'a', 'b', 'c'          Varargs and kwargs    a    b    c
    a\='1', b\=2           Varargs and kwargs    a=1    b=${2}
    'a', 'b\=b', c\='c'    Varargs and kwargs    a    b\=b    c=c

Embedded arguments
    [Documentation]    FAIL    Work but this fails
    Embedded arguments "work"
    embeDded ArgumeNtS "Work but this fails"

*** Keywords ***
Return value should be
    [Arguments]    ${expected}    ${keyword}    @{args}    &{kwargs}
    ${result} =    Run Keyword    ${keyword}    @{args}    &{kwargs}
    Should Be Equal    ${result}    ${expected}
