####!/bin/bash
cd ../frontend
npm run build
cd ../backend
ln -s ../front/dist static
export FLASK_ENV=production
flask run -p 1313
