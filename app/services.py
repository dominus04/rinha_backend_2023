def valida_dados(content) -> bool:
        if not content['nome'] or not content['apelido']:
            raise ValueError(422)
        
        if type(content['nome']) != str:
            raise TypeError(400)
        
        if content['stack'] and isinstance(content['stack'], list):
            for tech in content['stack']:
                if type(tech) != str or len(tech) > 32:
                    raise TypeError(400)
                