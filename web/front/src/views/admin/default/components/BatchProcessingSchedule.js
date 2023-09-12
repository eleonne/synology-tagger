// Chakra imports
import {
    SimpleGrid,
    Button,
    Flex,
    Icon,
    Text,
    useColorModeValue,
    Progress,
} from "@chakra-ui/react";
// Custom components
import axios from "axios"
import MiniStatistics from "components/card/MiniStatistics";
import IconBox from "components/icons/IconBox";
import React, { useState, useEffect, useCallback } from "react";
import useWebSocket, { ReadyState } from 'react-use-websocket';
// Assets
import {
    MdSchedule,
} from "react-icons/md";

export default function BatchProcessingSchedule(props) {
    const { ...rest } = props;
    const [socketUrl, setSocketUrl] = useState(process.env.REACT_APP_WS_URL + '/update-running-batch');
    const { sendMessage, lastMessage, readyState } = useWebSocket(socketUrl);

    const [state, setState] = useState({
        'start_date': '01/01/1900 às 00:00:00',
        'is_running': false,
        'pending_classification': 0,
        'error': {
            'error': 'false',
            'error_msg': ''
        }
    })

    useEffect(() => {
        if (lastMessage !== null) {
            const res = eval('(' + lastMessage.data + ')')
            setState({
                ...state,
                ...res.data
            })
        }
    }, [lastMessage]);

    const connectionStatus = {
        [ReadyState.CONNECTING]: 'Connecting',
        [ReadyState.OPEN]: 'Open',
        [ReadyState.CLOSING]: 'Closing',
        [ReadyState.CLOSED]: 'Closed',
        [ReadyState.UNINSTANTIATED]: 'Uninstantiated',
    }[readyState];



    const handleClickSendMessage = useCallback(() => {
        setState({
            ...state,
            'is_running': true,
        })
        axios.get(process.env.REACT_APP_API_URL + '/run-now').then(({ data }) => {
            if (data.error == 'true') {
                setState({
                    ...state,
                    'is_running': false,
                    error: {...data}
                })
            } else {
                setState({
                    ...state,
                    'is_running': true
                })
            }
        })
    });

    const boxBg = useColorModeValue("secondaryGray.300", "whiteAlpha.100");
    const brandColor = useColorModeValue("brand.500", "white");

    // const _endContent = 

    return (
        <SimpleGrid columns={{ base: 1, md: 1, xl: 1 }} gap='20px' mb='20px'>
            <MiniStatistics
                name='A próxima classificação está agendada para'
                textColorSecondary={brandColor}
                value={state.start_date}
                startContent={
                    <IconBox
                        w='56px'
                        h='56px'
                        bg={boxBg}
                        icon={
                            <Icon w='40px' h='40px' as={MdSchedule} color={brandColor} />
                        }
                    />
                }
                endContent={
                    <Flex align='flex-start' style={{ flexDirection: 'column', flex: 1 }}>
                        <Button
                            onClick={handleClickSendMessage}
                            // disabled={readyState !== ReadyState.OPEN}
                            mb='10px'
                            w='100%'
                            minW='140px'
                            mt={{ base: "20px", "2xl": "auto" }}
                            variant='brand'
                            isLoading={state.is_running === 'true'}
                            loadingText="Classificando"
                            fontWeight='500'>
                            Iniciar Classificação Agora!
                        </Button>
                        {
                            (state.error.error == 'true') ? <>
                                <Text
                                    color={brandColor}
                                    fontSize='14px'
                                    textAlign='start'
                                    fontWeight='700'
                                    lineHeight='100%'>
                                    {state.error.error_msg}
                                </Text>
                            </> : null
                        }
                        {
                            (state.is_running == 'true') ? <>
                                <Text
                                    color={brandColor}
                                    fontSize='14px'
                                    textAlign='start'
                                    fontWeight='700'
                                    lineHeight='100%'>
                                    Classificando imagens ({state.pending_classification}%)
                                </Text>
                                <Progress
                                    variant='table'
                                    colorScheme='brandScheme'
                                    h='8px'
                                    w='100%'
                                    value={state.pending_classification}
                                />
                            </> : null
                        }
                    </Flex>
                }
            />

        </SimpleGrid>
    );
}
