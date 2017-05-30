//
// Created by frivas on 3/04/17.
//

#include "RecorderInterface.h"



namespace recorder {

    RecorderInterface::RecorderInterface(std::vector<RecorderPoolPtr> &poolImages):
            poolImages(poolImages)
    {
    }

    bool RecorderInterface::saveLog(const ::std::string &name, ::Ice::Int seconds, const ::Ice::Current &ic)
    {
        bool ret = true;

        for (size_t i=0; i< poolImages.size(); i++)
        {


            poolWriteImagesPtr pool = boost::dynamic_pointer_cast<poolWriteImages> (poolImages[i]);
            bool log = pool->startCustomLog(name, seconds);
            ret = ret && log;
        }

        return ret;
    }

    bool RecorderInterface::saveVideo(const ::std::string &path, const ::std::string &name, ::Ice::Int seconds,
                                      const ::Ice::Current &ic) {
        bool ret = true;
        for (size_t i = 0; i < poolImages.size(); i++) {
            RecorderPoolPtr test;
            poolWriteImagesPtr pool = boost::dynamic_pointer_cast<poolWriteImages> (poolImages[i]);

            bool log = pool->startCustomVideo(path, name, seconds);
            ret = ret && log;
        }

        return ret;
    }



}