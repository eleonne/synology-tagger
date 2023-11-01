// Chakra imports
import {
    Box,
    Flex,
    Text,
    useColorModeValue,
} from "@chakra-ui/react";
// Custom components
import Card from "components/card/Card.js";
import {
    Table,
    Thead,
    Tbody,
    Tfoot,
    Tr,
    Th,
    Td,
    TableCaption,
} from "@chakra-ui/react"
import React, { useEffect, useState } from "react";
import { getChartOptions, getChartData, secondsToDhms } from '../../../../assets/utils'
import axios from "axios";
import { MdCheckCircle, MdSettings } from "react-icons/md";

export default function BatchProcessingTime(props) {
    const { ...rest } = props;

    const [state, setState] = useState({
        'data': []
    })

    useEffect(() => {
        axios.get(process.env.REACT_APP_BASE_URL + '/api/get-photos-by-country').then((response) => {
            setState({ 
                ...response.data
            })
        })
    }, []);

    const textColor = useColorModeValue("secondaryGray.900", "white");

    return (
        <Card
            justifyContent='center'
            align='center'
            direction='column'
            w='100%'
            mb='0px'
            {...rest}>
            <Flex justify='space-between' ps='0px' pe='20px' pt='5px'>
                <Flex align='center' w='100%'>
                    <Text color={textColor}
                        fontSize='34px'
                        textAlign='start'
                        fontWeight='700'
                        lineHeight='100%'>
                        Fotos por País
                    </Text>
                </Flex>
            </Flex>
            <Flex w='100%' flexDirection={{ base: "column", lg: "row" }} justifyContent='flex-start' alignItems='flex-start'>
                <Table variant="simple">
                    <Tbody>
                        {
                            (state.data.length === 0) ? null :
                                state.data.map((row) => {
                                    return <Tr>
                                        <Td>{row.label}</Td>
                                        <Td>{row.value.toLocaleString('pt-BR')}</Td>
                                    </Tr>
                                })
                        }
                    </Tbody>
                </Table>
            </Flex>
        </Card>
    );
}
