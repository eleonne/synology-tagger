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
import React, {useState, useEffect} from "react";
// Assets
import {
    MdSchedule,
} from "react-icons/md";

export default function BatchProcessingSchedule(props) {
    const { ...rest } = props;
    const [state, setState] = useState({
        'start_date': '01/01/1900 às 00:00:00',
        'is_running': false,
        'pending_classification': 0
    })

    useEffect(() => {
        axios.get(process.env.REACT_APP_BASE_URL + '/api/get-next-run').then((response) => {
            setState({
                ...state,
                ...response.data.data
            })
        })
    }, []);

    const boxBg = useColorModeValue("secondaryGray.300", "whiteAlpha.100");
    const brandColor = useColorModeValue("brand.500", "white");

    const _endContent = (state.is_running) ? <>
        <Text
            color={brandColor}
            fontSize='14px'
            textAlign='start'
            fontWeight='700'
            lineHeight='100%'>
            Classificando imagens (faltam {state.pending_classification}%)
        </Text>
        <Progress
            variant='table'
            colorScheme='brandScheme'
            h='8px'
            w='100%'
            value={state.pending_classification}
        />
    </> : null

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
                            mb='10px'
                            w='100%'
                            minW='140px'
                            mt={{ base: "20px", "2xl": "auto" }}
                            variant='brand'
                            isLoading={state.is_running}
                            loadingText="Classificando"
                            fontWeight='500'>
                            Iniciar Classificação Agora!
                        </Button>
                        {_endContent}
                    </Flex>
                }
            />

        </SimpleGrid>
    );
}
