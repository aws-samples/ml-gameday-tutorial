#! /usr/bin/env python
from invoke import invoke

height=10
width=10
if __name__ == "__main__":
    resp=invoke("ShootEndpoint",{
        "opponent":"test",
        "board":[[0]*width for x in range(height)],
    })
    print(resp)
