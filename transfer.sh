#!/bin/bash
# author: cunzhang
# time: 2021-07-10

old_gitlab_url='git@192.168.1.100'
new_gitlab_url='git@192.168.1.101'

file="group_projects.txt"


for line in `cat $file`
do
  array=(${line//\// })
  namespace=${array[0]}
  project=${array[1]}



  new=${new_gitlab_url}":"$namespace"/"$project".git"
  old=${old_gitlab_url}":"$namespace"/"$project".git"



  git clone $old || echo "##### Not have project or dir exist #######" >> clone.log

  sleep 1

  cd $project


  git branch -r|grep -v '\->'|while read remote
    do 
      git branch --track "${remote#origin/}" "$remote"
    done

  git branch|awk 'BEGIN{print "echo ****Update all local branch...***"}{if($1=="*"){current=substr($0,3)};print a"git checkout "substr($0,3);print "git pull --all";}END{print "git checkout " current}'|sh
  git remote rename origin old-origin
  git remote add origin $new
  git push -u origin --all
  git push -u origin --tags

  cd ..

  rm -rf $project
  echo "${array[0]},${array[1]}.git" >> succeed.txt

done
