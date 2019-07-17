#! /usr/bin/env python
from invoke import invoke

if __name__ == "__main__":
    resp=invoke("LayoutEndpoint",{
        "opponent":"test",
        "width":10,
        "height":10,
        "ruleSet":{
            "shipCells":10,
            "connectedShipCells":5
        }
    })
    print(resp)
