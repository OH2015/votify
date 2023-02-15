=== To run this application ===

・Install Docker and docker-compose commands
ex)yum install Docker docker-compose

・Execute next command
   docker-compose up -d


=== To development react files ===

・Install node.js in your PC
・Execute next command
   cd django/static/js
   npm install
   npm run watch

  Then whenever there is a change in the jsx file inside django/static/js/src it will be bundled into django/static/js/dist/bundle.js.

  
