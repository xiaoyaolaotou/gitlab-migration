#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: cunzhang
# Time: 2021-07-10

import gitlab
import os

old_gitlab = gitlab.Gitlab('http://192.168.1.100', private_token='hy7MNE7mLHMDeSGNsz7x', api_version='4')
new_gitlab = gitlab.Gitlab('http://192.168.1.101',private_token='ec67good2izmqSq42xAx', api_version='4')



# 获取所有组
def get_groups():
    groups=old_gitlab.groups.list(all=True,owned=True)
    for g in groups:
        with open('groups_all.txt','a') as f:
            print("获取项目组 %s 成功" %(g.name))
            f.write(g.name)
            f.write('\n')


# 创建项目组
def create_groups():
    with open('groups_all.txt','r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            try:
                new_gitlab.groups.create({'name':line,'path':line})
                print("创建项目组 %s 成功" %(line))
                with open('create_success.txt','a') as f:
                    f.write(line)
                    f.write('\n')
            except gitlab.exceptions.GitlabCreateError as e:
                    
                print("创建项目组 %s 失败,失败原因：%s" %(line,e))
                with open('create_failed.txt','a') as f:
                    f.write(line)
                    f.write('\n')


# 根据组获取项目
def get_projects():
    with open('group_projects.txt','a') as f:
        for g in old_gitlab.groups.list(all=True):
            for p in g.projects.list(all=True):
                print("group: %s, project: %s" %(g.name,p.name))
                # f.write(old + ':' + g.name + '/' + p.name + '.git')
                f.write(g.name + '/' + p.name)
                f.write('\n')
    

# push new git
def exec_shell():
    os.system('sh -x transfer.sh')
    


if __name__ == "__main__":
    get_groups()
    create_groups()
    get_projects()
    exec_shell()




   
