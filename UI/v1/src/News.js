import React from 'react';
import {
    Filter,
    TextInput,
    List,
    Datagrid,
    TextField,
} from 'react-admin';

const UrlField = ({ record, source, title }) => <a target="_blank" href={record[source]}>{record[title]}</a>;

const NewsFilter = (props) => (
    <Filter {...props}>
        <TextInput label="Search" source="q" alwaysOn />
    </Filter>
);

export const NewsList = props => (
    <List {...props} bulkActions={false} filters={<NewsFilter />} sort={{ field: 'Date', order: 'ASC' }}>
        <Datagrid hasBulkActions={false} >
            <TextField source="Source" />
            <UrlField label="Link" source="URL" title="Title"/>
        </Datagrid>
    </List>
);