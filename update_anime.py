#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Created on 2016/2/17 15:30.
import os
import time
import zipfile
import shutil

from logtools import logger
from apscheduler.schedulers.blocking import BlockingScheduler

src_dir = '/tmp/upload'
bak_dir = '/tmp/bakup'
dst_dir = '/tmp/dst'


def my_job():
    logger.info(u"开始本次运行....")
    try:
        # 判断是否存在需要解压的文件
        logger.info(u'判断是否存在需要解压更新的文件')
        os.chdir(src_dir)
        filenames = os.listdir(src_dir)
        logger.info(filenames)
        if filenames:
            for filename in filenames:
                logger.info(u'开始更新%s文件' % filename)
                with zipfile.ZipFile(filename, mode='r') as zipfiles:
                    zipfiles.extractall(path=None)

                # 重命名文件,并移动到备份目录
                file_bak = os.path.splitext(filename)[0] + '_' + time.strftime('%Y%m%d%H%M%S') + '.zip'
                os.rename(filename, file_bak)
                shutil.move(file_bak, bak_dir)

                # 切换工作目录
                tmp_dir = os.path.splitext(filename)[0]
                os.chdir(tmp_dir)
                # 如果存在.svn目录,则删除
                if os.path.exists('.svn'):
                    shutil.rmtree('.svn')

                # 将新文件copy到指定目录下面
                cmd = 'cp -rfvu ./* %s' % dst_dir
                # cmd = 'mv -uf ./* %s' % dst_dir
                os.system(cmd)

                # 返回上级目录
                os.chdir(src_dir)
                shutil.rmtree(tmp_dir)
                time.sleep(1)
                logger.info(u"更新%s完成.....\n" % filename)
        else:
            logger.info(u'不存在需要更新文件,退出本次任务....\n')
    except Exception as e:
        logger.info("The app is stoped.")
        logger.exception(e)


sched = BlockingScheduler()
'''interval 间隔调度
它的参数如下：
weeks (int) – number of weeks to wait
days (int) – number of days to wait
hours (int) – number of hours to wait
minutes (int) – number of minutes to wait
seconds (int) – number of seconds to wait
'''
# 任务多久重复执行一次
# sched.add_job(my_job, 'interval', minutes=5)
sched.add_job(my_job, 'interval', seconds=5)
sched.start()



