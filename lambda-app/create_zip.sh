#!/bin/bash
cd package
zip -r ../lambda_function.zip .
cd ..
zip lambda_function.zip *.py