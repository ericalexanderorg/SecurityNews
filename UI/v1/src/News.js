import React from 'react';
import {
    Filter,
    TextInput,
    BooleanInput,
    List,
    Datagrid,
    TextField,
    DateField,
    NumberField
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

const CveNewsFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
        <BooleanInput label="Has CVSS" source="HasCVSS" alwaysOn />
    </Filter>
);

export const CveNewsList = props => {
    const isSmall = useMediaQuery(theme => theme.breakpoints.down('sm'));
    return (
        <List {...props} bulkActionButtons={false} bulkActions={false} filters={<CveNewsFilter />} sort={{ field: 'Date', order: 'DESC' }} perPage={25}>
            {isSmall ? (
                <Datagrid hasBulkActions={false} >
                    <UrlField label="Link" source="URL" title="Title"/>
                </Datagrid>
            ) : (
                <Datagrid hasBulkActions={false} >
                    <TextField source="Impacts" label="Impacts (best guess)"/>
                    <UrlField label="Description" source="URL" title="Title"/>
                    <NumberField source="CVSS" label="CVSS"/>
                    <TextField source="Source" />
                    <DateField source="Date"/>
                </Datagrid>
            )}
        </List>
    );
};

