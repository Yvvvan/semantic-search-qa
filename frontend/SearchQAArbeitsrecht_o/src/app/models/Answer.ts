export class Answer
{
    type:string;//KW, SEMANTIC
    id:number;
    score:number;
    body:string;
    link:string;


    constructor(type, id, score, body, link)
    {
        this.type=type
        this.id = id;
        this.score = score;
        this.link = body;
    }

    /**
     * 	{
     *      fragen:[
     *              {
     *                  type:KW,
     *                  id:65, 
     *                  score:5.1637645,
     *                  body:Können Sie mit Ihrem Auftraggeber das Arbeitsrecht ausschließen? ,
     *                  link:https://www.hensche.de/Rechtsanwalt_Arbeitsrecht_Handbuch_Arbeitnehmer.html
     *              },
     *              {
     * ...]}

     */

}