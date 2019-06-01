import graphene
from graphene.relay import Node
from graphql import GraphQLError
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from api.gigs.models import Gig as GigModel

class Gig(MongoengineObjectType):
    """
        Get all Gigs
    """
    class Meta:
        model = GigModel
        interfaces = (Node,)

class CreateGig(graphene.Mutation):
    """
        Creates a new gig
    """
    class Arguments:
        title = graphene.String(required=True)
        price = graphene.String(required=True)
        description = graphene.String(required=True)
        contact_phone = graphene.String(required=True)
        contact_email = graphene.String(required=True)
        contact_name = graphene.String(required=True)
        location = graphene.String(required=True)
        category = graphene.String(required=True)

    gig = graphene.Field(Gig)

    def mutate(self, info, **kwargs):
        gig = GigModel(
            title=kwargs['title'],
            price=kwargs['price'],
            description=kwargs['description'],
            contact_phone=kwargs['contact_phone'],
            contact_email=kwargs['contact_email'],
            contact_name=kwargs['contact_name'],
            location=kwargs['location'],
            category=kwargs['category']
        )
        gig.save()
        if gig:
            return CreateGig(gig=gig)
        return GraphQLError("Action Failed")

class GigsList(graphene.ObjectType):
    gigs = graphene.List(Gig,
                         description="Returns all gigs")

class Query(graphene.ObjectType):
    get_all_gigs = graphene.Field(GigsList,
                                  limit=graphene.Int(),
                                  offset=graphene.Int(),
                                  description="Returns all gigs and takes the following arguments\
                                  \n- limit: Amount of gigs to return\
                                  \n- offset: Amount of gigs to skip")

    get_gigs_by_location = graphene.Field(GigsList,
                                       limit=graphene.Int(),
                                       offset=graphene.Int(),
                                       location=graphene.String(),
                                       description="Returns all gigs and takes the following arguments\
                                       \n- limit: Amount of gigs to return\
                                       \n- offset: Amount of gigs to skip\
                                       \n- location: Location to search from")
    
    get_gigs_by_category = graphene.Field(GigsList,
                                       limit=graphene.Int(),
                                       offset=graphene.Int(),
                                       category=graphene.String(),
                                       description="Returns all gigs and takes the following arguments\
                                       \n- limit: Amount of gigs to return\
                                       \n- offset: Amount of gigs to skip\
                                       \n- category: category to search for")

    def resolve_get_all_gigs(self, info, **kwargs):
        limit = kwargs['limit']
        offset = kwargs['offset']
        gigs = list(GigModel.objects.skip(offset).limit(limit))
        return GigsList(gigs=gigs)

    def resolve_get_gigs_by_location(self, info, **kwargs):
        limit = kwargs['limit']
        offset = kwargs['offset']
        location = kwargs['location']
        gigs = list(GigModel.objects(location=location).skip(offset).limit(limit))
        return GigsList(gigs=gigs)

    def resolve_get_gigs_by_category(self, info, **kwargs):
        limit = kwargs['limit']
        offset = kwargs['offset']
        category = kwargs['category']
        gigs = list(GigModel.objects(category=category).skip(offset).limit(limit))
        return GigsList(gigs=gigs)

class Mutation(graphene.ObjectType):
    create_gig = CreateGig.Field(
        description="Creates a new gig and takes the arguments\
            [required]\n- title: title of the gig[required]\
            [required]\n- price: Price of the gig[required]\
            [required]\n- desription: description of the gig[required]\
            [required]\n- contact_email: email of creator[required]\
            [required]\n- contact_name: name of creator[required]\
            [required]\n- contact_phone: phone number of creator[required]\
            [required]\n- location: location of the gig[required]\
            [required]\n- category: category of the gig[required]")


schema = graphene.Schema(query=Query, mutation=Mutation)
