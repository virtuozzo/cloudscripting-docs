# Template Basics

The above two units display the outer side of JPS usage and now let’s have a closer look at the inner side - the code of the package with all required configurations.

JPS manifest is a file with .json extension which contains an appropriate code written in JSON format (JSON Formatter & Validator). This manifest file includes the links to the web only dependencies. This file can be named as you require. 

The code should contain a set of strings needed for successful installation of application. The basis of the code is represented by the following strings:

```
{
    "jpsType": "installation type",
    "jpsVersion": "minimum engine version",
    "application": "JSON string"
}
```

This is a mandatory body part of the application package which includes the information about JPS version and the type of the application installation (“install” mode initiates a new environment creation required for deploy).
These basic strings should be extended with the settings required by the application you are packing. The following configuration details are included to the "application": { } parameter: