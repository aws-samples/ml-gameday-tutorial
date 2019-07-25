var base=require('../../config')
var _=require('lodash')

module.exports=Object.assign(base,{
    "parameters":_.pick(base.parameters,["MasterAccount","GameArchiveBucket"])
})

console.log(module.exports)
