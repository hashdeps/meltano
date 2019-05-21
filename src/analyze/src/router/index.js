import Router from 'vue-router';
import Vue from 'vue';


import EntitiesSelectorModal from '@/components/orchestration/EntitiesSelectorModal';
import Entities from '@/components/orchestration/Entities';
import Extractors from '@/components/orchestration/Extractors';
import ExtractorSettingsModal from '@/components/orchestration/ExtractorSettingsModal';
import Loaders from '@/components/orchestration/Loaders';
import LoaderSettingsModal from '@/components/orchestration/LoaderSettingsModal';
import RunSummary from '@/components/orchestration/RunSummary';

import Design from '@/views/Design';
import Designs from '@/views/Designs';
import Dashboards from '@/views/Dashboards';
import NotFound from '@/views/NotFound';
import Pipelines from '@/views/Pipelines';
import Repo from '@/views/Repo';

Vue.use(Router);

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '*',
      name: '404',
      component: NotFound,
    },
    {
      path: '/',
      redirect: '/pipelines',
    },
    {
      path: '/pipelines/',
      redirect: '/pipelines/extractors/',
      name: 'dataSetup',
      component: Pipelines,
      children: [
        {
          path: 'extractors',
          name: 'extractors',
          components: {
            default: Extractors,
          },
          meta: {
            isModal: false,
          },
        },
        {
          path: 'extractors/:extractor',
          name: 'extractorSettings',
          components: {
            default: Extractors,
            extractorSettings: ExtractorSettingsModal,
          },
          meta: {
            isModal: true,
          },
        },
        {
          path: 'entities',
          name: 'entities',
          components: {
            default: Entities,
          },
          meta: {
            isModal: false,
          },
        },
        {
          path: 'entities/:extractor',
          name: 'extractorEntities',
          components: {
            default: Entities,
            extractorEntities: EntitiesSelectorModal,
          },
          meta: {
            isModal: true,
          },
        },
        {
          path: 'loaders',
          name: 'loaders',
          components: {
            default: Loaders,
          },
          meta: {
            isModal: false,
          },
        },
        {
          path: 'loaders/:loader',
          name: 'loaderSettings',
          components: {
            default: Loaders,
            loaderSettings: LoaderSettingsModal,
          },
          meta: {
            isModal: true,
          },
        },
        {
          path: 'run',
          name: 'run',
          component: RunSummary,
        },
      ],
    },
    {
      path: '/files/',
      name: 'projectFiles',
      component: Repo,
    },
    {
      path: '/analyze/',
      name: 'analyze',
      component: Designs,
    },
    {
      path: '/analyze/:model/:design',
      name: 'analyze_design',
      component: Design,
    },
    {
      path: '/analyze/:model/:design/reports/report/:slug',
      name: 'Report',
      component: Design,
    },
    {
      path: '/dashboards/',
      name: 'Dashboards',
      component: Dashboards,
    },
    {
      path: '/dashboards/dashboard/:slug',
      name: 'Dashboard',
      component: Dashboards,
    },
  ],
});

export default router;
