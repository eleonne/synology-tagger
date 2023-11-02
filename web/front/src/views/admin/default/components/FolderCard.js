// Chakra imports
import {
    Box,
    Flex,
    Text,
    useColorModeValue,
    Icon
} from "@chakra-ui/react";
import IconBox from "components/icons/IconBox";
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
import { formatBytes } from '../../../../assets/utils'
import axios from "axios";
import { MdFolder, MdSettings } from "react-icons/md";

export default function FolderCard(props) {
    const { ...rest } = props;

    const [state, setState] = useState({
        'data': []
    })

    useEffect(() => {
        axios.get(process.env.REACT_APP_BASE_URL + '/api/get-bytes-by-folder').then((response) => {
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
                        Espaço por Pasta
                    </Text>
                </Flex>
            </Flex>
            <Flex w='100%' flexDirection={{ base: "column", lg: "row" }} justifyContent='flex-start' alignItems='flex-start'>
                <Box maxW="100%" maxH="300px" overflow="auto">
                    <Table variant="simple" variant="striped" size="md">
                        <Thead>
                            <Tr>
                                <Th>Pasta</Th>
                                <Th isNumeric>Total</Th>
                                <Th isNumeric>Videos</Th>
                                <Th isNumeric>Aux Videos</Th>
                                <Th isNumeric>Fotos</Th>
                                <Th isNumeric>Aux Fotos</Th>
                                <Th isNumeric>Total Media</Th>
                                <Th isNumeric>Total Aux</Th>
                            </Tr>
                        </Thead>
                        <Tbody>
                            {
                                (state.data.length === 0) ? null :
                                    state.data.map((row) => {
                                        return <Tr>
                                            <Td>
                                                <Flex w='100%' flexDirection={{ base: "column", lg: "row" }} justifyContent='flex-start' alignItems='center'>
                                                <IconBox
                                                    w='56px'
                                                    h='56px'
                                                    icon={
                                                        <Icon w='32px' h='32px' as={MdFolder} color='black' />
                                                    }
                                                />
                                                {row.folder}
                                                </Flex>
                                            </Td>
                                            <Td>{formatBytes(parseInt(row.major_videos_filesize) + parseInt(row.major_photos_filesize) + parseInt(row.aux_photos_filesize) + parseInt(row.aux_videos_filesize))}</Td>
                                            <Td>{formatBytes(row.major_videos_filesize)}</Td>
                                            <Td>{formatBytes(row.aux_videos_filesize)}</Td>
                                            <Td>{formatBytes(row.major_photos_filesize)}</Td>
                                            <Td>{formatBytes(row.aux_photos_filesize)}</Td>

                                            <Td>{formatBytes(parseInt(row.major_videos_filesize) + parseInt(row.major_photos_filesize))}</Td>
                                            <Td>{formatBytes(parseInt(row.aux_photos_filesize) + parseInt(row.aux_videos_filesize))}</Td>
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
