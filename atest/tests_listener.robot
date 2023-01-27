*** Settings ***
Library     ListenerCore.py


*** Test Cases ***
Tests The Keyword Argument
    [Documentation]    This test case tests that the keyword argument is equal
    ...    to the keyword argument from start_keyword.
    ...
    ...    It uses the core lib as listener.
    Listener Core    This is the first Argument

Tests The Test Name
    [Documentation]    This test case tests that the test case name is equal
    ...    to the test name from start_test.
    ...
    ...    It uses a component as listener.
    Second Component    Tests The Test Name

Tests The Suite Name
    [Documentation]    This test case tests that the suite name is equal
    ...    to the suite name from _start_suite.
    ...
    ...    It uses an independent class as listener which is manually set.
    First Component    Tests Listener
