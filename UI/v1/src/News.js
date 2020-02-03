import React from 'react';
import {
    Filter,
    TextInput,
    List,
    Datagrid,
    TextField,
    DateField
} from 'react-admin';
import { useMediaQuery } from '@material-ui/core';

const UrlField = ({ record, source, title }) => <a target="_blank" rel="noopener noreferrer" href={record[source]}>{record[title]}</a>;

const NewsFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
    </Filter>
);

export const NewsList = props => {
    const isSmall = useMediaQuery(theme => theme.breakpoints.down('sm'));
    return (
        <List {...props} bulkActionButtons={false} bulkActions={false} filters={<NewsFilter />} sort={{ field: 'Date', order: 'DESC' }} perPage={25}>
            {isSmall ? (
                <Datagrid hasBulkActions={false} >
                    <UrlField label="Link" source="URL" title="Title"/>
                </Datagrid>
            ) : (
                <Datagrid hasBulkActions={false} >
                    <UrlField label="Link" source="URL" title="Title"/>
                    <TextField source="Source" />
                    <DateField source="Date"/>
                </Datagrid>
            )}
        </List>
    );
};

export const CveNewsList = props => {
    const isSmall = useMediaQuery(theme => theme.breakpoints.down('sm'));
    return (
        <List {...props} bulkActionButtons={false} bulkActions={false} filters={<NewsFilter />} sort={{ field: 'Date', order: 'DESC' }} perPage={25}>
            {isSmall ? (
                <Datagrid hasBulkActions={false} >
                    <UrlField label="Link" source="URL" title="Title"/>
                </Datagrid>
            ) : (
                <Datagrid hasBulkActions={false} >
                    <TextField source="Impacts" label="Impacts (best guess)"/>
                    <UrlField label="Link" source="URL" title="Title"/>
                    <TextField source="Source" />
                    <DateField source="Date"/>
                </Datagrid>
            )}
        </List>
    );
};

