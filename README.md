## Instrution
1. If it is the **first time** to run this server, using the following command: `docker-compose up`

2. Otherwise, if you have alreay done the indexing step for ES, please **delete the comment symbol** at **line 44** in **docker-compose.yml**. This deletion will reset the entrypoint of IndexES, so that it will not run indexing again. After deletion, please run `docker-compose up`. (This step makes no big difference, but can help to save time)

3. visiting **localhost:4200** (This site can be visited after `mysearch` started, it is no need to wait for the whole indexing progress / `myindex`).
---
## Discription
With the command `docker-compose up`, four containers will be build, `myelastic`, `myfrontend`, `myindex` and `mysearch`. After building, they will start automaticlly at the same time. 

Firstly, `myelastic` and `myfrontend` will start at the beginning. `myelastic` is the server for Elastic Search and `myfrontend` is for Web Interface. These two containers need time to start (about 30 seconds).

Meanwhile, `mysearch` waits for 10 seconds. And then it tries to start. If `myelastic` starts successfully in this 10 seconds, `mysearch` will also successfully connected to ES. Otherwise, `mysearch` will try to restart itself, until the connection is established.

`myindex` waits 45 seconds. It also need `myelastic` to start. But because it cannot be restarted*, So it should only start if `myelastic` succeeds. But there is no detection, so what we can do is making the waiting time longer. 



