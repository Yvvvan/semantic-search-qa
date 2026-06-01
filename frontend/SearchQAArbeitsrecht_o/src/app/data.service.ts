import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class DataService{

  private REST_API_SERVER ='';// "http://localhost:5000/search/";

  constructor(private httpClient: HttpClient) { }

  public sendGetRequest(endpoint,param){
    param = param.replace(" ","+");
    this.REST_API_SERVER = endpoint+param;
    console.log("my request:"+this.REST_API_SERVER);
    return this.httpClient.get(this.REST_API_SERVER);
  }
}
