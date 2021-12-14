import "bootstrap"

import "@fortawesome/fontawesome-free/js/fontawesome"
import "@fortawesome/fontawesome-free/js/solid"
//import "@fortawesome/fontawesome-free/js/regular"
//import "@fortawesome/fontawesome-free/js/brands"

import {TabulatorFull as Tabulator} from "tabulator-tables";

import hljs from "highlight.js/lib/core";
import python from "highlight.js/lib/languages/python";
hljs.registerLanguage("python", python);

import "../scss/main.scss"



function getTopData(){
    return fetch("./assets/top.json")
           .then(response => response.json())
}

function init(){
    getTopData().then(data => {
        console.log(data)
        var table = new Tabulator("#table", {
                data: data,
                placeholder:"<span>Loading Data</span>",
                pagination: true,
                paginationMode: "local",
                layout:"fitColumns",
                tooltips:true,
                paginationSize: 5,
                movableColumns:false,
                resizableRows:true,
                columns:[
                    {
                        title:"Question",
                        field:"question",
                        formatter:"textarea",
                        sorter:"string",
                        vertAlign: "middle",
                        widthGrow: 3
                    },
                    {
                        title:"Answer",
                        field:"answer",
                        formatter:"html",
                        sorter:"number",
                        hozAlign:"center",
                        vertAlign: "middle",
                        widthGrow: 1,
                    },
                    {
                        title:"Codex Program",
                        field:"codex_output",
                        mutator:(value, data, type, params, component) => {
                            if(value){
                                value = value.replace(/#(.+)/gm, "")
                                value = value.replace(/'''[^]*?'''/gm, "")
                                value = value.replace(/^\s*\n/gm, "")
                            }
                            return value
                        },
                        formatter:(cell, formatterParams, onRendered) => {
                            cell.getElement().style.whiteSpace = "pre-wrap";
                            return hljs.highlight(cell.getValue(), {language: "python"}).value
                        },
                        sorter:"string",
                        widthGrow: 3,
                    },
                    {
                        title:"Program Output",
                        field:"program_execution_output",
                        formatter:"textarea",
                        sorter:"string",
                        hozAlign:"center",
                        vertAlign: "middle",
                        widthGrow: 1,
                    },
                    {
                        title:"Program Correct",
                        field:"is_execution_output_correct",
                        formatter:"tickCross",
                        formatterParams:{
                            allowEmpty:true,
                            allowTruthy:true,
                            tickElement:"<i class='fa fa-check' style='color: green'></i>",
                            crossElement:"<i class='fa fa-times' style='color:red'></i>",
                        },
                        sorter:"boolean",
                        hozAlign:"center",
                        vertAlign: "middle",
                        widthGrow: 1,
                    },
                    {
                        title:"GPT3 Output",
                        field:"gpt3_output",
                        formatter:"textarea",
                        sorter:"string",
                        widthGrow: 3,
                    },
                    {
                        title:"GPT3 Correct",
                        field:"is_gpt3_output_correct",
                        formatter:"tickCross",
                        formatterParams:{
                            allowEmpty:true,
                            allowTruthy:true,
                            tickElement:"<i class='fa fa-check' style='color: green'></i>",
                            crossElement:"<i class='fa fa-times' style='color:red'></i>",
                        },
                        sorter:"boolean",
                        hozAlign:"center",
                        vertAlign: "middle",
                        widthGrow: 1
                    },
                ],
            })
    })
}

init()