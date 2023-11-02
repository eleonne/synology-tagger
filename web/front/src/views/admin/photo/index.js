import {
    SimpleGrid,
} from "@chakra-ui/react";
// Custom components
import React, { useEffect, useState } from "react";
import PhotoTrend from "views/admin/default/components/PhotoTrend";
import VideoTrend from "views/admin/default/components/VideoTrend";
import MediaPie from "views/admin/default/components/MediaPie";
import CountryCard from "views/admin/default/components/CountryCard";
import CountryPie from "views/admin/default/components/CountryPie";
import { secondsToDhms, formatBytes, formatNumbers } from '../../../assets/utils'
import banner from "assets/img/auth/banner.png";
import eduardo from "assets/img/avatars/eduardo.jpeg";
import eliane from "assets/img/avatars/eliane.jpeg";
import Banner from "views/admin/default/components/Banner";
import FolderCard from "views/admin/default/components/FolderCard";
import FolderPie from "views/admin/default/components/FolderPie";
import axios from "axios";

export default function ClassifiedMediaVolume(props) {

    // const [state, setState] = useState({
    //     'labels': null,
    //     'values': null,
    //     'total': 0
    // })

    // useEffect(() => {
    //     axios.get(process.env.REACT_APP_BASE_URL + '/api/get-video-trend').then((response) => {
    //         const res = {
    //             'labels': getChartOptions(response.data.data.labels, chartId),
    //             'values': getChartData(response.data.data.values, "Tempo em segs"),
    //             'total': response.data.data.total
    //         }
    //         setState({ ...res })
    //     })
    // }, []);

    return (
        <>
            <SimpleGrid columns={{ base: 1, md: 1, xl: 1 }} gap='20px' mb='20px'>
                <SimpleGrid columns={{ base: 1, md: 2, xl: 2 }} gap='20px' mb='20px'>   
                    
                    <Banner
                        gridArea='1 / 1 / 2 / 2'
                        banner={banner}
                        avatar={eduardo}
                        name='Eduardo Leonne'
                        photos='17'
                        videos='9700'
                        usedSpace='274'
                    />
                    <Banner
                        gridArea='5 / 2 / 2 / 2'
                        banner={banner}
                        avatar={eliane}
                        name='Eliane Candida'
                        photos='17'
                        videos='9700000000000000000'
                        usedSpace='274'
                    />
                </SimpleGrid>
                <SimpleGrid columns={{ base: 1, md: 2, xl: 2 }} gap='20px' mb='20px'>  
                    <VideoTrend />
                    <PhotoTrend />                    
                </SimpleGrid>
                <SimpleGrid columns={{ base: 1, md: 3, xl: 3 }} gap='20px' mb='20px'>
                    <MediaPie title='Número de Vídeos' column='count' formatter={(val) => {
                        return formatNumbers(val)
                    }} />
                    <MediaPie title='Duração dos Vídeos' column='duration' formatter={(val) => {
                        return secondsToDhms(val)
                    }} />
                    <MediaPie title='Tamanho dos Vídeos' column='filesize' formatter={(val) => {
                        return formatBytes(val)
                    }} />
                </SimpleGrid>

                <SimpleGrid columns={{ base: 1, md: 2, xl: 2 }} gap='20px' mb='20px'>
                    <FolderCard />
                    <FolderPie  formatter={(val) => {
                        return formatBytes(val)
                    }} />
                </SimpleGrid>

                <SimpleGrid columns={{ base: 1, md: 2, xl: 2 }} gap='20px' mb='20px'>
                    <CountryCard />
                    <CountryPie  formatter={(val) => {
                        return formatNumbers(val)
                    }} />
                </SimpleGrid>

            </SimpleGrid>
        </>
    )
}