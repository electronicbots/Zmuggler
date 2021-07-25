## Introduction

Zmuggler, a simple tool for finding HTTP Request Smuggling vulnerability in a website. It works by providing the target URL. You can read this [article](https://electronicbots.gitbook.io/z0ldyck/web-application-security/http-request-smuggling) to learn more about HTTP Request Smuggling.

## Features

Zmuggler Features:

- Check for CL.TE
- Check for TE.CL
- Obfuscating Transfer-Encoding header

## Installation

Run the following commands:
```
$ git clone https://github.com/electronicbots/Zmuggler.git
$ pip3 install -r requirements.txt
$ chmod +x Zmuggler.py
```

## Usage

![Usage](https://github.com/electronicbots/Zmuggler/blob/main/images/9.png)

## Example

```
./Zmuggler.py --target <target_URL>
```
