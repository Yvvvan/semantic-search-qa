import { Component, Input } from '@angular/core';
//import { HttpClient } from '@angular/common/http';
import { Answer } from './models/Answer';
import { DataService } from './data.service';
import { environment } from './../environments/environment';

// Project maintainers, 2021.

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = 'SearchQAArbeitsrecht';

  IsAsked:boolean=false;
  semanticchecked = true;
  kwchecked = true;

  kwresult = [];
  semanticresult = [];
  filterkwresult = [];
  filtersemanticresult = [];
  filterkwscorehi=0;
  filtersmscorehi=0;
  filtervaluekw=0;
  filtervaluesm=0;
  filterstepkw=1;
  filterstepsm=1;
  inputQ:string = "";
  inputQfeedback:string="";
  endpoint:string = environment.APIEndpoint;
  
  // scrolling
  GetDataSpec1() {
    this.inputQ = "Wann bekomme ich eine Abfindung mit Beispiel dazu?";
    this.GetData();
  }
  GetDataSpec2() {
    this.inputQ = "Habe ich Anspruch auf Dienstwagen?";
    this.GetData();
  }
  GetDataSpec3() {
    this.inputQ = "Wo finde ich Information zu Elternzeit?";
    this.GetData();
  }
  GetDataSpec4() {
    this.inputQ = "Darf ich Urlaub während der Probezeit nehmen?";
    this.GetData();
  }

  // get result
  constructor(private dataServie : DataService){}
  GetData(){
    if (this.inputQ.length === 0) {
      return
    }
    if (this.inputQ.charAt(0)== '#') {
      this.inputQ = this.inputQ.replace('#','')
    }
    //reset
    this.inputQ = this.inputQ.replace('/',' ')
    this.inputQ = this.inputQ.replace('\\',' ')
    this.kwresult=[]
    this.semanticresult=[]
    this.filterkwresult = [];
    this.filtersemanticresult = [];
    this.filterkwscorehi=0;
    this.filtersmscorehi=0;
    this.filtervaluekw=0;
    this.filtervaluesm=0;
    this.filterstepkw=1;
    this.filterstepsm=1;
    this.IsAsked = true;

    this.dataServie.sendGetRequest(this.endpoint, this.inputQ)
    .subscribe((data: Answer[]) =>{
      //console.log(data);
      const objJSON = JSON.parse(data.toString());
      console.log(objJSON);
    
    //kw:  key=1,2,3.... the index of the result
    for (var key in objJSON.kw){
      this.kwresult.push(
        objJSON.kw[key]
      );
    };
    // if there is no kw result
    if (this.kwresult.length <= 0) {
      if (objJSON.lang == "de"){
        this.kwresult.push(
          JSON.parse('{"type":"Fehler","id": 0,"score": 0,  "body": "Keyword Nicht Gefunden",  "body2": "Bitte verwenden Sie andere Suchbegriffe.", "link": " " }')
       );
      }
      else{
        this.kwresult.push(
          JSON.parse('{"type":"Fehler","id": 0,"score": 0,  "body": "Eingabesprache Nicht Unterstützt",  "body2": "Bitte verwenden Sie andere Suchbegriffe. Keyword Search unterstützt nur die folgende Sprache: <br><ul><li>Deutsch</li></ul>", "link": " " }')
       );
      }
      
    }
    // find the maximum of score
    this.filterkwscorehi = Math.floor(this.kwresult[0]["score"]);
    if (this.filterkwscorehi<5){
      this.filterstepkw = this.filterkwscorehi/5;
    }
    
    // add score color
    this.setColor(this.kwresult,objJSON.kwscore);

    this.filterkwresult = this.kwresult;

    //--------------------------------------------------
    //semantic:   key=1,2,3.... the index of the result
    for (var key in objJSON.semantic){
      this.semanticresult.push(
        objJSON.semantic[key]
      );  
    };
    // if there is no kw result
    if (this.semanticresult.length <= 0) {
      this.semanticresult.push(
        JSON.parse('{"type":"Fehler","id": 0,"score": 0,  "body": "Eingabesprache Nicht Unterstützt",  "body2": "Bitte verwenden Sie andere Suchbegriffe. Semantic Search unterstützt nur die folgenden Sprachen: <br><ul><li>Arabisch</li><li>Chinesisch (vereinfacht)</li><li>Chinesisch (traditionell)</li><li>Deutsch</li><li>Englisch</li><li>Französisch</li><li>Italienisch</li><li>Japanisch</li><li>Koreanisch</li><li>Niederländisch</li><li>Polnisch</li><li>Portugiesisch</li><li>Spanisch</li><li>Thai</li><li>Türkisch</li><li>Russisch</li></ul>", "link": " " }')
     );
    }
    // find the maximum of score
    this.filtersmscorehi = Math.floor(this.semanticresult[0]["score"]);
    if (this.filtersmscorehi<5){
      this.filterstepsm = this.filtersmscorehi/5;
    }
    // add score color
    this.setColor(this.semanticresult,objJSON.smscore);

    this.filtersemanticresult = this.semanticresult;
    });

    //--------------------------------------------------
    

    // skip to this location
    location.href = "#result";

    //reset
    this.inputQfeedback = this.inputQ;
    this.inputQ = "";
  }

  // filter-button
  FilterDatakw(){
    this.filterkwresult = this.kwresult.filter(t=>t.score >=this.filtervaluekw);
  }
  FilterDatasm(){
    this.filtersemanticresult = this.semanticresult.filter(t=>t.score >=this.filtervaluesm);
  }
  
  // slider
  getSliderValuekw(event) {
    this.filtervaluekw=event.target.value;
  }
  getSliderValuesm(event) {
    this.filtervaluesm=event.target.value;
  }

  colormode=2;
  setColor(result,scorelayer){
    var str = scorelayer.split(",")
    let lay1 = str[0].split("[")[1];
    let lay2 = str[1].split("]")[0];
    
    // score-based---------
    // if(this.colormode==1){
    //   const min = result[result.length-1]["score"];
    //   const max = result[0]["score"];
    //   const step = (max-min)/3
    //   lay1 = min+step;
    //   lay2 = max-step;
    // }
    // sequence-based--------
    // else{
    //   let key1= Math.min(
    //     result.length-1,
    //     Math.round(result.length*0.73));
    //   lay1 = result[key1]["score"];

    //   let key2= Math.round(result.length*0.27);
    //   lay2 = result[key2]["score"];
    // }
    // set color
    for (var key in result){
      result[key]["color"]="btn-primary";
      if(result[key]["score"] >= lay2){
        result[key]["color"]="btn-danger";
      }
      else if (result[key]["score"] > lay1){
        result[key]["color"]="btn-warning";
      }
      if (result[key]["score"]==0){
        result[key]["color"]="btn-primary";
      }
    }
  }

  
}
