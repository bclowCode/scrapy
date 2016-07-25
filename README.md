# scrapy
scrapy example

base on 1.1 turtorial

execute:
scrapy crawl  bcSpider  -o myout.json

01-moz-dir : simple download (use n9)
02-moz-dir-persists : test /persistance (use dmoz directly) 
  * question need to clarify:
    1. ctrl-c need 2 times
      * can't ctrl-C for 2 times
      * http://stackoverflow.com/questions/28851535/how-does-scrapy-pause-resume-work
      * -o myout.json will broken : empty result (we migth need save our result to external storage)
        * ctrl-c 1 time is okay
    1. ctrl-c won't stop the cralwer immediately, usually it take ~ 1 min to gracefully stop 
      * (How to deal with the crash on production?) 
    1. ref: http://www.open-open.com/lib/view/open1419683400953.html
03-mod-dir-return-request-and-item (use n9)
  * use 2 seed 
  * maintain referral, seed and depth by our own
  * turn on cache and turn off robot
04-mod-dir-use-crawler (use n9)
