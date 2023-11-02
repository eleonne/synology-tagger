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
import { formatNumbers } from '../../../../assets/utils'
import axios from "axios";

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
                <Box w="100%" maxW="100%" maxH="300px" overflow="auto">
                    <Table variant="simple" variant="striped" size="lg">
                        <Thead>
                            <Tr>
                                <Th>País</Th>
                                <Th isNumeric>-</Th>
                            </Tr>
                        </Thead>
                        <Tbody>
                            {
                                (state.data.length === 0) ? null :
                                    state.data.map((row) => {
                                        return <Tr>
                                            <Td>{row.label}</Td>
                                            <Td>{formatNumbers(row.value)}</Td>
                                        </Tr>
                                    })
                            }
                        </Tbody>
                    </Table>
                </Box>
            </Flex>
        </Card>
    );
}
