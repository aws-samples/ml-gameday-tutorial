var base=require('../../config')
var _=require('lodash')

module.exports=_.defaults({
    project:base.project+"-bootstrap",
    parameters:{}
},base)
