import{d,r as l,w as r,v as a,a as p,i,o as u}from"./index-bab582ff.js";const f=["onKeydown"],v=d({__name:"index",setup(g){const t=l({editContent:"",editing:!1}),s=o=>{if(o.preventDefault(),t.editing){console.log("editing, cancel send");return}console.log("send")};return(o,e)=>r((u(),p("textarea",{"onUpdate:modelValue":e[0]||(e[0]=n=>t.editContent=n),contenteditable:"",class:"flex-1 p-2 b-gray-300 b-solid b-2 rounded-lg",onCompositionstart:e[1]||(e[1]=()=>t.editing=!0),onCompositionend:e[2]||(e[2]=()=>t.editing=!1),onKeyup:e[3]||(e[3]=i(n=>n.preventDefault(),["enter"])),onKeydown:i(s,["enter"])},null,40,f)),[[a,t.editContent]])}});export{v as default};
