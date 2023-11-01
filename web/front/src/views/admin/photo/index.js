import {
    SimpleGrid,
  } from "@chakra-ui/react";
  // Custom components
import React from "react";
import PhotoTrend from "views/admin/default/components/PhotoTrend";
import VideoTrend from "views/admin/default/components/VideoTrend";
import MyPie from "views/admin/default/components/MyPie";
import CountryCard from "views/admin/default/components/CountryCard";
import Member from "components/card/Member";
import {secondsToDhms, formatBytes} from '../../../assets/utils'
import banner from "assets/img/auth/banner.png";
import avatar from "assets/img/avatars/avatar4.png";
import Banner from "views/admin/profile/components/Banner";

export default function ClassifiedMediaVolume(props) {
    return (
        <>
            <SimpleGrid columns={{ base: 1, md: 1, xl: 1 }} gap='20px' mb='20px'>
                <PhotoTrend />
                <VideoTrend />
                <SimpleGrid columns={{ base: 1, md: 3, xl: 3 }} gap='20px' mb='20px'>
                    <MyPie title='Número de Vídeos' column='count' />
                    <MyPie title='Duração dos Vídeos' column='duration' formatter={(val) => {
                        return secondsToDhms(val)
                    }}/>
                    <MyPie title='Tamanho dos Vídeos' column='filesize'  formatter={(val) => {
                        return formatBytes(val)
                    }}/>
                </SimpleGrid>

                <SimpleGrid columns={{ base: 1, md: 3, xl: 3 }} gap='20px' mb='20px'>
                    <CountryCard />
                    {/* <Banner
                        gridArea='1 / 1 / 2 / 2'
                        banner={banner}
                        avatar={avatar}
                        name='Adela Parkson'
                        job='Product Designer'
                        posts='17'
                        followers='9.7k'
                        following='274'
                        />
                    <Banner
                        gridArea='1 / 1 / 2 / 2'
                        banner={banner}
                        avatar={avatar}
                        name='Adela Parkson'
                        job='Product Designer'
                        posts='17'
                        followers='9.7k'
                        following='274'
                        /> */}

                </SimpleGrid>
                
            </SimpleGrid>
        </>
    )
}