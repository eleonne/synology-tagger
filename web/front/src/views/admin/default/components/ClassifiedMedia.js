// Custom components
import MiniStatistics from "components/card/MiniStatistics";
import IconBox from "components/icons/IconBox";
import axios from "axios";
import React, {useEffect, useState} from "react";
import {secondsToDhms} from '../../../../assets/utils'

import {
    useColorModeValue,
    Icon,
    SimpleGrid,
} from "@chakra-ui/react";
import {
    MdPermMedia,
    MdOutlineVideocam,
    MdOutlineVideocamOff,
    MdImage,
    MdBrokenImage,
} from "react-icons/md";

export default function ClassifiedMedia(props) {
    const {brandColor, boxBg} = props;

    const [state, setState] = useState({
        "classified_total": 0,
        "classified_images": 0,
        "classified_short_videos": 0,
        "classified_videos": 0,
        "classified_long_videos": 0, 
        "unclassified_total": 0,
        "unclassified_images": 0,
        "unclassified_short_videos": 0,
        "unclassified_videos": 0,
        "unclassified_long_videos": 0,
        "unclassified_total_color": '#25be93',
        "unclassified_images_color": '#25be93',
        "unclassified_short_videos_color": '#25be93',
        "unclassified_videos_color": '#25be93',
        "unclassified_long_videos_color": '#25be93',
        "unclassified_total_color_weak": '#a8e5d4',
        "unclassified_images_color_weak": '#a8e5d4',
        "unclassified_short_videos_color_weak": '#a8e5d4',
        "unclassified_videos_color_weak": '#a8e5d4',
        "unclassified_long_videos_color_weak": '#a8e5d4',
    });
  
    useEffect(() => {
        axios.get(process.env.REACT_APP_BASE_URL + '/api/get-totals').then((response) => {
            setState(response.data.data)
        })
    }, []);

    useEffect((props) => {
        setState({
            ...state,
            "unclassified_total_color": (state.unclassified_total > 0) ? '#df92a8' : '#25be93',
            "unclassified_images_color": (state.unclassified_images > 0) ? '#df92a8' : '#25be93',
            "unclassified_short_videos_color": (state.unclassified_short_videos > 0) ? '#df92a8' : '#25be93',
            "unclassified_videos_color": (state.unclassified_videos > 0) ? '#df92a8' : '#25be93',
            "unclassified_long_videos_color": (state.unclassified_long_videos > 0) ? '#df92a8' : '#25be93',
            "unclassified_total_color_weak": (state.unclassified_total > 0) ? '#e5a8b9' : '#a8e5d4',
            "unclassified_images_color_weak": (state.unclassified_images > 0) ? '#e5a8b9' : '#a8e5d4',
            "unclassified_short_videos_color_weak": (state.unclassified_short_videos > 0) ? '#e5a8b9' : '#a8e5d4',
            "unclassified_videos_color_weak": (state.unclassified_videos > 0) ? '#e5a8b9' : '#a8e5d4',
            "unclassified_long_videos_color_weak": (state.unclassified_long_videos > 0) ? '#e5a8b9' : '#a8e5d4',
        })
    }, [state.unclassified_total])

    return (

        <>
            <SimpleGrid columns={{ base: 1, md: 2, xl: 2 }} gap='20px' mb='20px'>
                <MiniStatistics
                    name='Total de Arquivos Classificados'
                    value={(state.classified_total).toLocaleString('pt-BR')}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={boxBg}
                        icon={
                            <Icon w='32px' h='32px' as={MdPermMedia} color={brandColor} />
                        }
                        />
                    }
                />
                <MiniStatistics
                    name='Total de Arquivos não Classificados'
                    textColorSecondary='white'
                    value={(state.unclassified_total).toLocaleString('pt-BR')}
                    bg={state.unclassified_total_color}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={state.unclassified_total_color_weak}
                        icon={
                            <Icon w='32px' h='32px' as={MdBrokenImage} color='white' />
                        }
                        />
                    }
                />
            </SimpleGrid>
            <SimpleGrid
                columns={{ base: 1, md: 2, lg: 4, "2xl": 4 }}
                gap='20px'
                mb='20px'>
                <MiniStatistics
                    name='Imagens Classificadas'
                    value={(state.classified_images).toLocaleString('pt-BR')}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={boxBg}
                        icon={
                            <Icon w='32px' h='32px' as={MdImage} color={brandColor} />
                        }
                        />
                    }
                />
                <MiniStatistics
                    name='Videos Curtos Classificados (até 20s)'
                    value={secondsToDhms(state.classified_short_videos)}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={boxBg}
                        icon={<Icon w='28px' h='28px' as={MdOutlineVideocam} color={brandColor} />}
                        />
                    }
                />
                <MiniStatistics
                    name='Videos Classificados (entre 1-5mins)'
                    value={secondsToDhms(state.classified_videos)}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={boxBg}
                        icon={<Icon w='28px' h='28px' as={MdOutlineVideocam} color={brandColor} />}
                        />
                    }
                />
                <MiniStatistics
                    name='Videos Longos Classificados (maior que 5mins)'
                    value={secondsToDhms(state.classified_long_videos)}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={boxBg}
                        icon={<Icon w='40px' h='40px' as={MdOutlineVideocam} color={brandColor} />}
                        />
                    }
                />
                <MiniStatistics
                    name='Imagens não Classificadas'
                    textColorSecondary='white'
                    value={(state.unclassified_images).toLocaleString('pt-BR')}
                    bg={state.unclassified_images_color}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={state.unclassified_images_color_weak}
                        icon={
                            <Icon w='32px' h='32px' as={MdBrokenImage} color='white' />
                        }
                        />
                    }
                />
                <MiniStatistics
                    name='Videos Curtos não Classificados (até 20s)'
                    textColorSecondary='white'
                    value={secondsToDhms(state.unclassified_short_videos)}
                    bg={state.unclassified_short_videos_color}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={state.unclassified_short_videos_color_weak}
                        icon={
                            <Icon w='32px' h='32px' as={MdOutlineVideocamOff} color='white' />
                        }
                        />
                    }
                />
                <MiniStatistics
                    name='Videos não Classificados (entre 1-5mins)'
                    textColorSecondary='white'
                    value={secondsToDhms(state.unclassified_videos)}
                    bg={state.unclassified_videos_color}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={state.unclassified_videos_color_weak}
                        icon={
                            <Icon w='40px' h='40px' as={MdOutlineVideocamOff} color='white' />
                        }
                        />
                    }
                />
                <MiniStatistics
                    name='Videos Longos Classificados (maior que 5mins)'
                    textColorSecondary='white'
                    value={secondsToDhms(state.unclassified_long_videos)}
                    bg={state.unclassified_long_videos_color}
                    startContent={
                        <IconBox
                        w='56px'
                        h='56px'
                        bg={state.unclassified_long_videos_color_weak}
                        icon={
                            <Icon w='40px' h='40px' as={MdOutlineVideocamOff} color='white' />
                        }
                        />
                    }
                />
            </SimpleGrid>
        </>
    )
}